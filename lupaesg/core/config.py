from typing import Optional, Dict, Any
from pydantic_settings import BaseSettings
from functools import lru_cache
import logging
from enum import Enum

class EnvironmentType(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class Settings(BaseSettings):
    # Ambiente
    ENVIRONMENT: EnvironmentType = EnvironmentType.DEVELOPMENT
    DEBUG: bool = True
    APP_NAME: str = "LupaESG"
    APP_VERSION: str = "0.1.0"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # MongoDB
    MONGODB_URL: str
    MONGODB_DATABASE: str
    MONGODB_MAX_POOL_SIZE: int = 10
    MONGODB_MIN_POOL_SIZE: int = 1
    
    # AWS S3
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: Optional[str] = None
    S3_BUCKET_NAME: Optional[str] = None
    
    # APIs
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "text-embedding-3-small"
    GEMINI_API_KEY: Optional[str] = None
    
    # Pinecone
    PINECONE_API_KEY: Optional[str] = None
    PINECONE_ENVIRONMENT: Optional[str] = None
    PINECONE_INDEX_NAME: Optional[str] = None
    
    # Telegram (para alertas)
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    TELEGRAM_CHAT_ID: Optional[str] = None
    
    # Logging
    LOG_LEVEL: int = logging.INFO
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Cache
    CACHE_TTL: int = 3600  # 1 hora em segundos
    
    # Limites e Quotas
    MAX_REQUESTS_PER_MINUTE: int = 60
    MAX_CONCURRENT_DOWNLOADS: int = 5
    
    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == EnvironmentType.DEVELOPMENT
    
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == EnvironmentType.PRODUCTION
    
    def get_mongodb_settings(self) -> Dict[str, Any]:
        return {
            "host": self.MONGODB_URL,
            "maxPoolSize": self.MONGODB_MAX_POOL_SIZE,
            "minPoolSize": self.MONGODB_MIN_POOL_SIZE,
        }
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()

# Exemplo de uso do logger configurado com base nas settings
def setup_logger(name: str = None) -> logging.Logger:
    logger = logging.getLogger(name or settings.APP_NAME)
    logger.setLevel(settings.LOG_LEVEL)
    
    formatter = logging.Formatter(settings.LOG_FORMAT)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    return logger