import re

from ai_service.models import ClassificationResponse


class RuleBasedClassificationProvider:
    _INCIDENT_WORDS = frozenset(
        {
            "down",
            "error",
            "failed",
            "failure",
            "outage",
            "unavailable",
        }
    )

    _ACCESS_WORDS = frozenset(
        {
            "access",
            "permission",
            "permissions",
            "role",
        }
    )

    def classify(self, text: str) -> ClassificationResponse:
        words = set(re.findall(r"[a-z0-9_]+", text.casefold()))

        if words & self._INCIDENT_WORDS:
            return ClassificationResponse(
                category="incident",
                confidence=0.90,
            )

        if words & self._ACCESS_WORDS:
            return ClassificationResponse(
                category="access_request",
                confidence=0.85,
            )

        if text.rstrip().endswith("?"):
            return ClassificationResponse(
                category="question",
                confidence=0.75,
            )

        return ClassificationResponse(
            category="other",
            confidence=0.50,
        )
