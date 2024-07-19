class ChatService:
    async def generate_response(self, query: str) -> str:
        if not query:
            raise ValueError("Query must not be empty")
        return f"This is a mock response to: {query}"
