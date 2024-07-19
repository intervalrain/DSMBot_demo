from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "DSM Bot"

    class Config:
        env_file = ".env"

settings = Settings()
