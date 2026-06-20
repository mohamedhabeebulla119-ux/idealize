import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    CHROMA_DB_DIR: str = os.getenv("CHROMA_DB_DIR", "vector_db/chroma_db")

    class Config:
        env_file = ".env"

settings = Settings()
