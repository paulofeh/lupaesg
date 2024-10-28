from typing import Optional
from pymongo import MongoClient
from pymongo.database import Database
from .config import get_settings
from .logging import setup_logger

logger = setup_logger(__name__)

class MongoDB:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.initialized = False
        return cls._instance
    
    def __init__(self):
        if self.initialized:
            return
            
        self.settings = get_settings()
        self._client: Optional[MongoClient] = None
        self._db: Optional[Database] = None
        logger.debug("MongoDB manager initialized with database: %s", self.settings.mongodb_database)
        self.initialized = True
    
    def connect(self) -> Database:
        """Connect to MongoDB and return database instance."""
        if not self._client:
            logger.info("Establishing new MongoDB connection...")
            try:
                self._client = MongoClient(self.settings.mongodb_url)
                self._db = self._client[self.settings.mongodb_database]
                # Testa a conexão
                self._client.server_info()
                logger.info("MongoDB connection established successfully")
            except Exception as e:
                logger.error("Failed to connect to MongoDB: %s", str(e))
                raise
        return self._db
    
    def close(self):
        """Close MongoDB connection."""
        if self._client:
            logger.info("Closing MongoDB connection...")
            try:
                self._client.close()
                self._client = None
                self._db = None
                logger.info("MongoDB connection closed")
            except Exception as e:
                logger.error("Error closing MongoDB connection: %s", str(e))
                raise
    
    @property
    def db(self) -> Database:
        """Get database instance, connecting if necessary."""
        if not self._db:
            return self.connect()
        return self._db

def get_mongodb() -> MongoDB:
    """Get MongoDB instance (singleton)."""
    return MongoDB()