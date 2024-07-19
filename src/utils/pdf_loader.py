import os
import logging
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_pdfs_from_directory(directory_path):
    documents = []
    for filename in os.listdir(directory_path):
        if filename.endswith('.pdf'):
            file_path = os.path.join(directory_path, filename)
            try:
                pdf = PdfReader(file_path)
                text = ""
                for page in pdf.pages:
                    text += page.extract_text()
                documents.append({"content": text, "metadata": {"source": filename}})
                logger.info(f"Successfully loaded {filename}")
            except Exception as e:
                logger.error(f"Error loading {filename}: {str(e)}")
    logger.info(f"Loaded {len(documents)} documents in total")
    return documents

def split_documents(documents, chunk_size=1000, chunk_overlap=200):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    splits = []
    for doc in documents:
        docs = text_splitter.create_documents([doc['content']], metadatas=[doc['metadata']])
        splits.extend(docs)
    logger.info(f"Split documents into {len(splits)} chunks")
    return splits