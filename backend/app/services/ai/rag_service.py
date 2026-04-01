import chromadb

# Mock setup: In production, you would point this to a persistent directory
# client = chromadb.PersistentClient(path="./data/chroma_db")
# For testing our AI voice pipeline without keys/documents, we use an ephemeral one:

client = chromadb.Client()

# Initialize a collection for Indian Emergency Protocols
try:
    collection = client.get_or_create_collection("emergency_protocols")
except Exception:
    collection = None

def get_rag_context(query_text: str) -> str:
    """Fetches relevant context from ChromaDB based on user transcript."""
    if not collection:
        return ""
        
    try:
        # Mocking empty count for now. Will execute true search later.
        if collection.count() == 0:
            return ""
            
        results = collection.query(
            query_texts=[query_text],
            n_results=2
        )
        
        # Merge documents if any were found
        if results['documents'] and len(results['documents']) > 0:
            return " ".join(results['documents'][0])
    except Exception as e:
        print(f"RAG Error: {e}")
        return ""
