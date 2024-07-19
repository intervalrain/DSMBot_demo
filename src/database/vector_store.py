import chromadb
from chromadb.config import Settings

class VectorStore:
    def __init__(self):
        self.client = chromadb.Client(Settings(allow_reset=True))
        self.collection = self.client.create_collection("product_manuals")

    async def add_documents(self, documents, metadatas, ids):
        self.collection.add(documents=documents, metadatas=metadatas, ids=ids)

    async def search(self, query, n_results=5):
        results = self.collection.query(query_texts=[query], n_results=n_results)
        return results
    
vector_store = VectorStore()
vector_store.add_documents(
    documents=["This is a sample document", "Annother sample manual"],
    metadatas=[{"tech": "22ehv", "tech": "22ulp"}],
    ids=["1","2"]
)