"""ChromaDB-backed evidence storage."""

from pathlib import Path
from typing import Any

from app.config import settings


class VectorStoreService:
    def __init__(
        self,
        persistent_path: str | Path | None = None,
        collection_name: str | None = None,
        model_name: str | None = None,
    ):
        import chromadb
        from chromadb.utils import embedding_functions

        storage_path = Path(persistent_path or settings.chroma_path)
        storage_path.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=str(storage_path))
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=model_name or settings.embedding_model
        )
        self.collection = self.client.get_or_create_collection(
            name=collection_name or settings.collection_name,
            embedding_function=self.embedding_fn
        )

    def add_document(self, doc_id: str, content: str) -> int:
        chunks = self._chunk_content(content)

        ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [
            {"doc_id": doc_id, "chunk_index": i} for i in range(len(chunks))
        ]

        self.collection.upsert(
            documents=chunks,
            ids=ids,
            metadatas=metadatas
        )
        return len(chunks)

    def query_similarity(self, query_text: str, n_results: int = 1) -> dict[str, Any]:
        if self.collection.count() == 0:
            return {"documents": [[]], "distances": [[]], "metadatas": [[]]}
        results = self.collection.query(
            query_texts=[query_text],
            n_results=max(1, n_results),
        )
        return results

    @staticmethod
    def _chunk_content(content: str) -> list[str]:
        paragraphs = [part.strip() for part in content.split("\n\n") if part.strip()]
        if not paragraphs:
            return [content.strip()]

        chunks: list[str] = []
        for paragraph in paragraphs:
            for start in range(0, len(paragraph), settings.max_chunk_characters):
                chunk = paragraph[start:start + settings.max_chunk_characters].strip()
                if chunk:
                    chunks.append(chunk)
        return chunks