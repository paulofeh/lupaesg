from functools import lru_cache
from typing import Optional
from pydantic import BaseModel

class Settings(BaseModel):
    """Base settings for the application."""
    # App settings
    environment: str = "development"
    debug: bool = True
    app_name: str = "LupaESG"
    app_version: str = "0.1.0"
    
    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    
    # MongoDB settings
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_database: str = "lupaesg"
    
    # AWS settings
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_region: str = "sa-east-1"
    s3_bucket_name: Optional[str] = None
    
    # OpenAI settings
    openai_api_key: Optional[str] = None
    openai_model: str = "text-embedding-3-small"
    
    # Pinecone settings
    pinecone_api_key: Optional[str] = None
    pinecone_index_name: Optional[str] = None

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    """Get application settings."""
    return Settings()