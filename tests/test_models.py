import pytest
from pydantic import ValidationError

from ai_service.models import ClassificationRequest, ClassificationResponse


def test_classification_request_strips_whitespace() -> None:
    request = ClassificationRequest(text= " production is unavailable ")

    assert request.text == "production is unavailable"

@pytest.mark.parametrize(
    "text",
    [
        "",
        "   ",
        "x" * 2_001,
    ],
)
def test_classification_request_rejects_invalid_text(text: str) -> None:
    with pytest.raises(ValidationError):
        ClassificationRequest(text=text)


@pytest.mark.parametrize("confidence", [-0.1, 1.1])
def test_classification_response_rejects_invalid_confidence(
    confidence: float,
) -> None:
    with pytest.raises(ValidationError):
        ClassificationResponse(
            category="incident",
            confidence=confidence
        )
