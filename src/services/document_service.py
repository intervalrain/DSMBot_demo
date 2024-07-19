import logging
from src.utils.pdf_loader import load_pdfs_from_directory, split_documents
from src.database.vector_store import vector_store

logger = logging.getLogger(__name__)

class DocumentService:
    @staticmethod
    async def load_and_index_documents(directory_path):
        logger.info(f"Starting to load documents from {directory_path}")
        documents = load_pdfs_from_directory(directory_path)
        splits = split_documents(documents)
        vector_store.add_documents(splits)
        logger.info(f"Finished indexing {len(splits)} document chunks")
        return len(splits)

document_service = DocumentService()