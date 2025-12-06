import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any, Optional
from app.core.config import settings

class VectorStore:
    def add_documents(self, documents: List[str], metadatas: List[Dict[str, Any]], ids: List[str], embeddings: List[List[float]]):
        raise NotImplementedError

    def query(self, query_embeddings: List[List[float]], n_results: int = 5):
        raise NotImplementedError

class ChromaVectorStore(VectorStore):
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.CHROMA_DB_DIR)
        self.collection = self.client.get_or_create_collection(name="documents")

    def add_documents(self, documents: List[str], metadatas: List[Dict[str, Any]], ids: List[str], embeddings: List[List[float]]):
        self.collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def query(self, query_embeddings: List[List[float]], n_results: int = 5):
        return self.collection.query(
            query_embeddings=query_embeddings,
            n_results=n_results
        )

def get_vector_store() -> VectorStore:
    # Factory function to get the configured vector store
    if settings.VECTOR_DB_TYPE == "chroma":
        return ChromaVectorStore()
    # Placeholder for Pinecone
    raise NotImplementedError("Only ChromaDB is currently supported")
