from pydantic_settings import BaseSettings
from pydantic import Field, computed_field
from typing import Optional
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # Database settings
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: str = "3306"
    MYSQL_DATABASE: str
    
    # Redis settings
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_EXPIRE: int = 3600
    
    # Auth settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # First superuser
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str
    
    # Debug mode
    DEBUG: bool = False
    
    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+asyncmy://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"
    
    class Config:
        env_file = Path(__file__).parent.parent / ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = True
        extra = 'ignore'

settings = Settings()