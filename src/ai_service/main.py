from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel

class HealthResponse(BaseModel):
    status: Literal["ok"]
    service: str
    version: str

app = FastAPI(
    title="AI Engineering Journey",
    version="0.1.0",
)

@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service="ai-engineering-journey",
        version=app.version
    )