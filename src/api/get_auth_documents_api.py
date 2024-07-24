from fastapi import APIRouter, HTTPException, Depends
from src.services.doc_provider import DocProvider, get_doc_provider

router = APIRouter()

@router.get("/auth_documents")
async def get_auth_documents(doc_provider: DocProvider = Depends(get_doc_provider)):
    """
    Get the authorized documents for the user
    """
    try:
        user_id = "00053997"
        docs = doc_provider.get_docs(user_id)
        return {"documents": docs}
    except:
        raise HTTPException(status_code=500, detail=str(e))
    