from typing import Annotated, Literal

from fastapi import Depends, FastAPI
from pydantic import BaseModel

from ai_service.models import ClassificationRequest, ClassificationResponse
from ai_service.providers.base import ClassificationProvider
from ai_service.providers.rule_based import RuleBasedClassificationProvider


class HealthResponse(BaseModel):
    status: Literal["ok"]
    service: str
    version: str

app = FastAPI(
    title="AI Engineering Journey",
    version="0.1.0",
)

_classification_provider = RuleBasedClassificationProvider()

def get_classification_provider() -> ClassificationProvider:
    return _classification_provider

ClassificationProviderDependency = Annotated[
    ClassificationProvider,
    Depends(get_classification_provider),
]

@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service="ai-engineering-journey",
        version=app.version
    )

@app.post("/classify", response_model=ClassificationResponse)
def classify(
    request: ClassificationRequest,
    provider: ClassificationProviderDependency,
) -> ClassificationResponse:
    return provider.classify(request.text)
