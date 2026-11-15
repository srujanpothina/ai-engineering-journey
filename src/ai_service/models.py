from typing import Annotated, Literal

from pydantic import BaseModel, Field, StringConstraints

ClassificationText = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=2_000,
    )
]

ClassificationCategory = Literal[
    "incident",
    "access_request",
    "question",
    "other"
]

class ClassificationRequest(BaseModel):
    text: ClassificationText

class ClassificationResponse(BaseModel):
    category: ClassificationCategory
    confidence: float = Field(ge=0.0, le=1.0)
