import os
import logging
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from src.database.vector_store import VectorStore, get_vector_store
from src.api.chat_api import router as chat_router
from src.api.load_documents_api import router as load_documents_router
from src.api.get_document_status_api import router as get_document_status_router
from src.api.get_auth_documents_api import router as get_auth_documents_router  

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION)
logging.basicConfig(level=logging.INFO)

# 允許所有來源的 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 掛載靜態文件
app.mount("/web", StaticFiles(directory="web"), name="web")

# router
app.include_router(chat_router)
app.include_router(load_documents_router)
app.include_router(get_document_status_router)
app.include_router(get_auth_documents_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
