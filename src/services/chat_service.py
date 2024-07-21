import logging
from fastapi import Depends, HTTPException
from typing import List, Tuple
from src.database.vector_store import VectorStore
from src.services.llm_service import LocalLLM
from config import settings

logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self, vector_store: VectorStore, llm: LocalLLM):
        self.vector_store = vector_store
        self.llm = llm  
        self.conversation_history: List[Tuple[str, str]] = []
        
    async def generate_response(self, query: str) -> str:
        if not query:
            raise ValueError("Query must not be empty")
        
        try:
            self.conversation_history.append(("user", query))
            
            # 建構包含對話歷史的提示
            history_context = "\n".join([f"{role}: {msg}" for role, msg in self.conversation_history[-settings.HISTORY_LENGTH:]])
            
            # 檢查是否需要從向量庫中搜索
            need_search_prompt = f"""
            Human:
            基於以下對話歷史和當前問題，判斷是否需要搜索額外訊息來回答問題。
            如果需要，回答"yes"；如果不需要，直接回答問題。
            對話歷史: {history_context}
            當前問題: {query}
            是否需要搜索額外訊息: 
            """
            
            need_search_response = await self.llm.generate(need_search_prompt)
            need_search = need_search_response.strip().lower() == "yes"
            
            if need_search:
                # 執行向量搜索
                results = self.vector_store.search(query)
            
                if not results['documents'] or not results['documents'][0]:
                    logger.warning("No documents found in vector store search")
                    context = "我無法從提供的資訊中找到答案"
                else:
                    context = "\n".join(results['documents'][0])

                prompt = f"""
                        Human: 
                        使用以下資訊來回答問題。如果無法從資訊中找到答案，請說 "我無法從提供的資訊中找到答案"。
                        對話歷史：
                        {history_context}
                        
                        資訊:
                        {context}
        
                        問題: 
                        {query}
        
                        Assistant: 根據提供的資訊與歷史對話，我的回答是：
                        """
            else: 
                prompt = f"""
                Human:
                基於以下對話歷史，回答當前問題：
                對話歷史：
                {history_context}

                當前問題: 
                {query}

                Assistant: 我的回答是：
                """
                
            response = await self.llm.generate(prompt)
            self.conversation_history.append(("assistant", response.strip()))
            return response.strip()
        
        except Exception as e:
            logger.exception(f"An error occurred while generating response: {str(e)}")
            raise HTTPException(status_code=500, detail="An error occurred while processing your request")
    
    def get_conversation_history(self) -> List[Tuple[str, str]]:
        return self.conversation_history

def get_chat_service(
    vector_store: VectorStore = Depends(VectorStore),
    llm: LocalLLM = Depends(LocalLLM)
) -> ChatService:
    return ChatService(vector_store, llm)