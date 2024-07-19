from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "DSM Bot"
    DESCRIPTION: str = "A chatbot API for DSM"
    VERSION: str = "1.0.0"

    class Config:
        env_file = ".env"

settings = Settings()
