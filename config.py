import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    # app description
    PROJECT_NAME: str = "DSM Bot"
    DESCRIPTION: str = "A chatbot API for DSM"
    VERSION: str = "1.0.0"
    
    # secret key
    SECRET_KEY: str
    
    # app configuration
    PDF_DIRECTORY: str = "./docs"
    LLM_MODEL_NAME: str = "mistral"
    HISTORY_LENGTH: int = 5
    TOP_K: int = 5
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    class Config:
        env_file = ".env"

settings = Settings()
