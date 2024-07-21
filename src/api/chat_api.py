from fastapi import APIRouter, HTTPException, Depends
from contracts.chat_request import ChatRequest
from contracts.chat_response import ChatResponse
from src.services.chat_service import ChatService, get_chat_service

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service)):
    """
    Chat endpoint that generates a response based on the user's query.
    
    - **query**: The user's prompt
    """
    try:
        response = await chat_service.generate_response(request.query)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    