"""Evidence retrieval and deterministic claim classification."""

from app.services.vector_store import VectorStoreService
from app.config import settings
from app.models.schemas import VerificationStatus

class VerificationPipeline:
    def __init__(
        self,
        vector_store: VectorStoreService,
        threshold: float = settings.verification_threshold,
    ):
        self.vector_store = vector_store
        self.threshold = threshold

    def verify_claim(self, claim: str) -> dict:
        search_results = self.vector_store.query_similarity(claim, n_results=1)

        documents = search_results.get("documents", [[]])[0]
        distances = search_results.get("distances", [[]])[0]

        if not documents:
            return {
                "claim": claim,
                "status": VerificationStatus.UNVERIFIED,
                "confidence_score": 0.0,
                "source_excerpt": None
            }

        best_match = documents[0]
        distance = distances[0] if distances else 0.0

        # Convert distance to similarity score
        confidence = max(0.0, min(1.0, 1.0 - (float(distance) / 2.0)))

        status = (
            VerificationStatus.VERIFIED
            if confidence >= self.threshold
            else VerificationStatus.UNVERIFIED
        )

        return {
            "claim": claim,
            "status": status,
            "confidence_score": round(confidence, 2),
            "source_excerpt": best_match
        }