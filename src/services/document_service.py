import logging
from fastapi import Depends
from src.utils.pdf_loader import load_pdfs_from_directory, split_documents
from src.database.vector_store import VectorStore, get_vector_store

logger = logging.getLogger(__name__)

class DocumentService:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        
    async def load_and_index_documents(self, directory_path):
        logger.info(f"Starting to load documents from {directory_path}")
        documents = load_pdfs_from_directory(directory_path)
        splits = split_documents(documents)
        self.vector_store.add_documents(splits)
        logger.info(f"Finished indexing {len(splits)} document chunks")
        return len(splits)

def get_document_service(vector_store: VectorStore = Depends(get_vector_store)) -> DocumentService:
    return DocumentService(vector_store)