"""Application configuration loaded from environment variables."""

from dataclasses import dataclass
import os
from pathlib import Path


def _read_float(name: str, default: float) -> float:
    value = os.getenv(name)
    return default if value is None else float(value)


@dataclass(frozen=True)
class Settings:
    """Runtime settings for the API and vector store."""

    app_name: str = os.getenv("APP_NAME", "Claim Verification Microservice")
    app_version: str = os.getenv("APP_VERSION", "1.0.0")
    chroma_path: Path = Path(os.getenv("CHROMA_PATH", "./data/chroma_db"))
    collection_name: str = os.getenv("CHROMA_COLLECTION", "evidence_store")
    embedding_model: str = os.getenv(
        "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
    )
    verification_threshold: float = _read_float("VERIFICATION_THRESHOLD", 0.60)
    max_chunk_characters: int = int(os.getenv("MAX_CHUNK_CHARACTERS", "1200"))


settings = Settings()