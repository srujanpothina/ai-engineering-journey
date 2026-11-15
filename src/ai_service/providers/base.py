from typing import Protocol

from ai_service.models import ClassificationResponse


class ClassificationProvider(Protocol):
    def classify(self, text: str) -> ClassificationResponse:
        """Classify the supplied text."""
        ...
