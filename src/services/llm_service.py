from langchain_community.llms import Ollama
from config import settings

class LocalLLM:
    def __init__(self, model_name=settings.LLM_MODEL_NAME):
        self.llm = Ollama(model=model_name)

    async def generate(self, prompt: str) -> str:
        return self.llm.invoke(prompt)

def get_local_llm() -> LocalLLM:
    return LocalLLM() 