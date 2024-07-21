from fastapi import APIRouter, HTTPException, Depends
from src.database.vector_store import VectorStore, get_vector_store

router = APIRouter()

@router.get("/document-status")
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

