from src.database.vector_store import vector_store

class ChatService:
    async def generate_response(self, query: str) -> str:
        results = vector_store.search(query)
        if not query:
            raise ValueError("Query must not be empty")
        
        context = "\n".join(results['documents'][0])
        
        response = f"Based on the context: {context}\nHere's a mock response to: {query}"
        return response