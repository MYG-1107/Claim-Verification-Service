"""FastAPI application entrypoint."""

from functools import lru_cache

from fastapi import Depends, FastAPI, HTTPException, status

from app.config import settings
from app.models.schemas import (
    IngestRequest,
    IngestResponse,
    VerifyRequest,
    VerifyResponse,
)
from app.services.vector_store import VectorStoreService
from app.services.pipeline import VerificationPipeline

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Deterministic evidence extraction and claim verification service."
)


@lru_cache(maxsize=1)
def get_pipeline() -> VerificationPipeline:
    """Create the model-backed pipeline only when an endpoint needs it."""
    return VerificationPipeline(VectorStoreService())

@app.get("/")
def read_root():
    return {"status": "online", "service": settings.app_name}


@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/v1/ingest", response_model=IngestResponse)
def ingest_document(payload: IngestRequest, pipeline: VerificationPipeline = Depends(get_pipeline)):
    try:
        chunks_count = pipeline.vector_store.add_document(
            payload.document_id, payload.content
        )
        return IngestResponse(
            message="Document successfully processed and indexed.",
            chunks_created=chunks_count
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="The document could not be indexed.",
        ) from exc

@app.post("/api/v1/verify", response_model=VerifyResponse)
def verify_claim(payload: VerifyRequest, pipeline: VerificationPipeline = Depends(get_pipeline)):
    try:
        result = pipeline.verify_claim(payload.claim)
        return VerifyResponse(**result)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="The claim could not be verified.",
        ) from exc