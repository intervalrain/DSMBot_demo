from pydantic import BaseModel

class DocumentLoadResponse(BaseModel):
    message: str