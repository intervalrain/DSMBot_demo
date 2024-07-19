import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

class VectorStore:
    def __init__(self):
        self.client = chromadb.Client(Settings(allow_reset=True))
        self.collection = self.client.create_collection("DSM")
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

    def add_documents(self, documents):
        self.collection.add(
            documents=[doc.page_content for doc in documents], 
            metadatas=[doc.metadata for doc in documents], 
            ids=[f"doc_{i}" for i in range(len(documents))])

    def search(self, query, n_results=5):
        results = self.collection.query(query_texts=[query], n_results=n_results)
        return results
    
vector_store = VectorStore()