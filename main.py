from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
from contracts.chat_request import ChatRequest
from contracts.chat_response import ChatResponse
from contracts.document_load_response import DocumentLoadResponse
from src.config import settings
from src.services.chat_service import ChatService, get_chat_service
from src.services.document_service import DocumentService, get_document_service
from src.database.vector_store import VectorStore, get_vector_store

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

@app.post("/load-documents", response_model=DocumentLoadResponse)
async def load_documents(
    background_tasks: BackgroundTasks,
    document_service: DocumentService = Depends(get_document_service)):
    """
    Load and index PDF documents from a specified directory.
    """
    try:
        background_tasks.add_task(document_service.load_and_index_documents, settings.PDF_DIRECTORY)
        return DocumentLoadResponse(message="Document loading started in the background.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/document-status")
async def get_document_status(
    vector_store: VectorStore = Depends(get_vector_store)):
    """
    Get the current status of indexed documents.
    """
    try:
        doc_count = vector_store.collection.count()
        return {"indexed_documents": doc_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
