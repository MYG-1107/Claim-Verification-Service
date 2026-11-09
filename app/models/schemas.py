from pydantic import BaseModel, Field
from typing import Optional, List

class IngestRequest(BaseModel):
    document_id: str = Field(..., example="doc_001")
    content: str = Field(..., example="The company achieved a 15% revenue growth in Q3.")

class IngestResponse(BaseModel):
    status: str
    message: str
    chunks_created: int

class VerifyRequest(BaseModel):
    claim: str = Field(..., example="Company revenue grew by 15% in Q3.")

class VerifyResponse(BaseModel):
    claim: str
    status: str
    confidence_score: float
    source_excerpt: Optional[str] = None