from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from app.knowledge_base.health_data import HEALTH_KNOWLEDGE_BASE
import logging

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        self.db = None
        self._initialize()

    def _initialize(self):
        try:
            logger.info("Initializing RAG service...")

            embedding_model = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )

            documents = [
                Document(
                    page_content=text,
                    metadata={"source": "arohan_health_kb"}
                )
                for text in HEALTH_KNOWLEDGE_BASE
            ]

            self.db = Chroma.from_documents(
                documents,
                embedding_model,
                collection_name="arohan_health_knowledge"
            )

            logger.info(f"RAG ready — {len(documents)} documents embedded.")

        except Exception as e:
            logger.error(f"RAG init failed: {e}")
            raise

    def retrieve_context(self, query: str, k: int = 3) -> str:
        """Called by llm_service.py"""
        if not self.db:
            return ""
        try:
            results = self.db.similarity_search(query, k=k)
            return "\n\n".join([doc.page_content for doc in results])
        except Exception as e:
            logger.error(f"Retrieval failed: {e}")
            return ""


# Singleton instance
rag_service = RAGService()


# Called by agent_service.py
def get_rag_context(query: str) -> str:
    return rag_service.retrieve_context(query)