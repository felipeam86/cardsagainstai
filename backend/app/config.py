from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./cards_against_ai.db"
    REDIS_URL: str = "redis://localhost:6379"
    ANTHROPIC_API_KEY: str

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()