from typing import List, Tuple
from pydantic import BaseModel

class ChatResponse(BaseModel):
    response: str
    history: List[Tuple[str, str]]