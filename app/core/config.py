import os
from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./fresh_store.db"
    SECRET_KEY: str = "fresh_store_secret_key_2026_change_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    PROJECT_NAME: str = "生鲜称重连锁系统"
    PROJECT_VERSION: str = "1.0.0"
    DEBUG: bool = True

    class Config:
        env_file = BASE_DIR / ".env"

settings = Settings()
