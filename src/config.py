from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "DSM Bot"
    DESCRIPTION: str = "A chatbot API for DSM"
    VERSION: str = "1.0.0"
    PDF_DIRECTORY: str = "./docs"
    LLM_MODEL_NAME: str = "mistral"

    class Config:
        env_file = ".env"

settings = Settings()
