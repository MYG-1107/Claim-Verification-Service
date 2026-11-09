import chromadb
from chromadb.utils import embedding_functions

class VectorStoreService:
    def __init__(self, persistent_path: str = "./data/chroma_db"):
        self.client = chromadb.PersistentClient(path=persistent_path)
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        self.collection = self.client.get_or_create_collection(
            name="evidence_store",
            embedding_function=self.embedding_fn
        )

    def add_document(self, doc_id: str, content: str) -> int:
        # Simple paragraph chunking
        chunks = [c.strip() for c in content.split("\n\n") if c.strip()]
        if not chunks:
            chunks = [content]

        ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [{"doc_id": doc_id, "chunk_index": i} for i in range(len(chunks))]

        self.collection.add(
            documents=chunks,
            ids=ids,
            metadatas=metadatas
        )
        return len(chunks)

    def query_similarity(self, query_text: str, n_results: int = 1):
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results