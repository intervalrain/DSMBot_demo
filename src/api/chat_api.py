from fastapi import APIRouter, HTTPException, Depends
from typing import List, Tuple
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
        history = chat_service.get_conversation_history()
        return ChatResponse(response=response, history=history)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
    