from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from contracts.chat_request import ChatRequest
from contracts.chat_response import ChatResponse
from src.config import settings
from src.services.chat_service import ChatService

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION)

@app.get("/")
async def root():
    """
    Root endpoint that returns a welcome message.
    """
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, chat_service: ChatService = Depends(ChatService)):
    """
    Chat endpoint that generates a response based on the user's query.
    
    - **query**: The user's prompt
    """
    try:
        response = await chat_service.generate_response(request.query)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
