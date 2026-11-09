from fastapi import FastAPI, HTTPException
from app.models.schemas import IngestRequest, IngestResponse, VerifyRequest, VerifyResponse
from app.services.vector_store import VectorStoreService
from app.services.pipeline import VerificationPipeline

app = FastAPI(
    title="LLM Claim Verification Microservice",
    version="1.0.0",
    description="Deterministic evidence extraction and claim verification service."
)

vector_store = VectorStoreService()
pipeline = VerificationPipeline(vector_store)

@app.get("/")
def read_root():
    return {"status": "online", "service": "Claim Verification Microservice"}

@app.post("/api/v1/ingest", response_model=IngestResponse)
def ingest_document(payload: IngestRequest):
    try:
        chunks_count = vector_store.add_document(payload.document_id, payload.content)
        return IngestResponse(
            status="success",
            message="Document successfully processed and indexed.",
            chunks_created=chunks_count
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/verify", response_model=VerifyResponse)
def verify_claim(payload: VerifyRequest):
    try:
        result = pipeline.verify_claim(payload.claim)
        return VerifyResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))