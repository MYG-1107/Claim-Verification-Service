from fastapi.testclient import TestClient

from app.main import app, get_pipeline
from app.services.pipeline import VerificationPipeline


class FakeVectorStore:
    def __init__(self):
        self.documents = []

    def add_document(self, doc_id: str, content: str) -> int:
        self.documents.append((doc_id, content))
        return 1

    def query_similarity(self, query_text: str, n_results: int = 1):
        if not self.documents:
            return {"documents": [[]], "distances": [[]]}
        return {"documents": [[self.documents[0][1]]], "distances": [[0.2]]}


fake_pipeline = VerificationPipeline(FakeVectorStore())
app.dependency_overrides[get_pipeline] = lambda: fake_pipeline
client = TestClient(app)


def teardown_module():
    app.dependency_overrides.clear()


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_ingest_and_verify():
    ingest = client.post(
        "/api/v1/ingest",
        json={"document_id": "doc-1", "content": "Revenue grew by 15 percent."},
    )
    assert ingest.status_code == 200
    assert ingest.json()["chunks_created"] == 1

    verify = client.post(
        "/api/v1/verify",
        json={"claim": "Revenue grew by 15 percent."},
    )
    assert verify.status_code == 200
    assert verify.json()["status"] == "VERIFIED"
    assert verify.json()["confidence_score"] == 0.9


def test_validation_rejects_empty_claim():
    response = client.post("/api/v1/verify", json={"claim": ""})
    assert response.status_code == 422