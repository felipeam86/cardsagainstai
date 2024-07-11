from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./cards_against_ai.db"
    REDIS_URL: str = "redis://localhost:6379/0"
    # Add other configuration variables here

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
