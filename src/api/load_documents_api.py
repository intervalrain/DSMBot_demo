import os
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from contracts.document_load_response import DocumentLoadResponse
from config import settings
from src.services.document_service import DocumentService, get_document_service

router = APIRouter()

@router.post("/load-documents", response_model=DocumentLoadResponse)
async def load_documents(
    background_tasks: BackgroundTasks,
    document_service: DocumentService = Depends(get_document_service)):
    """
    Load and index PDF documents from a specified directory.
    """
    try:
        directory_path = settings.PDF_DIRECTORY
        if not os.path.exists(directory_path):
            raise HTTPException(status_code=404, detail="Directory not found")
        
        background_tasks.add_task(document_service.load_and_index_documents, settings.PDF_DIRECTORY)
        return DocumentLoadResponse(message="Document loading started in the background.")
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))