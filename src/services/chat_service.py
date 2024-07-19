from src.database.vector_store import vector_store

class ChatService:
    async def generate_response(self, query: str) -> str:
        results = await vector_store.search(query)
        if not query:
            raise ValueError("Query must not be empty")
        return f"Found documents: {results['documents']}"
