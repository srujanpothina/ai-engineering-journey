import pytest

from ai_service.providers.rule_based import RuleBasedClassificationProvider


@pytest.mark.parametrize(
    ("text", "expected_category", "expected_confidence"),
    [
        ("The production database is unavailable", "incident", 0.90),
        ("Please grant me access to the dashboard", "access_request", 0.85),
        ("How does this service work ?", "question", 0.75),
        ("The deployment completed successfully", "other", 0.50),
    ],
)
def test_rule_based_classification(
    text: str,
    expected_category: str,
    expected_confidence: float,
) -> None:
    provider = RuleBasedClassificationProvider()

    result = provider.classify(text)

    assert result.category == expected_category
    assert result.confidence == expected_confidence
