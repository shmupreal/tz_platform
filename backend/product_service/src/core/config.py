from functools import lru_cache
from typing import Literal
from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    AUTH_SERVICE_URL: str
    NOTIFICATION_SERVICE_URL: str

    POSTGRES_USER: str
    POSTGRES_PASS: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    
    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        extra = "allow"


@lru_cache()
def settings() -> Settings:
    return Settings()