from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class VerificationStatus(str, Enum):
    VERIFIED = "VERIFIED"
    UNVERIFIED = "UNVERIFIED"


class IngestRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    document_id: str = Field(..., min_length=1, max_length=200, examples=["doc_001"])
    content: str = Field(
        ..., min_length=1, max_length=1_000_000,
        examples=["The company achieved a 15% revenue growth in Q3."],
    )

class IngestResponse(BaseModel):
    status: str = "success"
    message: str
    chunks_created: int = Field(..., ge=1)

class VerifyRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    claim: str = Field(..., min_length=1, max_length=10_000,
                       examples=["Company revenue grew by 15% in Q3."])

class VerifyResponse(BaseModel):
    claim: str
    status: VerificationStatus
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    source_excerpt: Optional[str] = None