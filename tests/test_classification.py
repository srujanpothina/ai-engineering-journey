from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from ai_service.main import app, get_classification_provider
from ai_service.models import ClassificationResponse


@pytest.fixture
def client() -> Iterator[TestClient]:
    app.dependency_overrides.clear()

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

def test_classified_incident(client: TestClient) -> None:
    response = client.post(
        "/classify",
        json={
            "text": "The production database is unavailable"
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "category": "incident",
        "confidence": 0.9,
    }

@pytest.mark.parametrize("text", ["", "  "])
def test_rejects_blank_text(client: TestClient, text: str) -> None:
    response = client.post(
        "/classify",
        json = {
            "text": text
        },
    )

    assert response.status_code == 422

def test_uses_injected_provider(client: TestClient) -> None:
    class StubProvider:
        def classify(self, text: str) -> ClassificationResponse:
            return ClassificationResponse(
                category="other",
                confidence=1.0,
            )
    
    app.dependency_overrides[get_classification_provider] = StubProvider

    response = client.post(
        "/classify",
        json= {
            "text": "The database is unavailable"
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "category": "other",
        "confidence": 1.0,
    }