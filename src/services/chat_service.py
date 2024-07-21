from fastapi import Depends
from src.database.vector_store import VectorStore
from src.services.llm_service import LocalLLM

class ChatService:
    def __init__(self, vector_store: VectorStore, llm: LocalLLM):
        self.vector_store = vector_store
        self.llm = llm  
        
    async def generate_response(self, query: str) -> str:
        results = self.vector_store.search(query)
        if not query:
            raise ValueError("Query must not be empty")
        
        context = "\n".join(results['documents'][0])
        
        prompt = f"""Human: 使用以下資訊來回答問題。如果無法從資訊中找到答案，請說 "我無法從提供的資訊中找到答案"。

資訊:
{context}

問題: {query}

Assistant: 根據提供的資訊，我的回答是：
"""
        
        response = await self.llm.generate(prompt)
        return response.strip() 

def get_chat_service(
    vector_store: VectorStore = Depends(VectorStore),
    llm: LocalLLM = Depends(LocalLLM)
) -> ChatService:
    return ChatService(vector_store, llm)