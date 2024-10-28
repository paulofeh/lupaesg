# MongoDB connection configuration will go here

from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class MongoDB:
    client: AsyncIOMotorClient = None
    
    @classmethod
    async def connect_to_database(cls):
        """Cria a conexão com o MongoDB."""
        if cls.client is None:
            try:
                cls.client = AsyncIOMotorClient(settings.MONGODB_URL)
                print("Conectado ao MongoDB com sucesso!")
            except Exception as e:
                print(f"Erro ao conectar ao MongoDB: {e}")
                raise e

    @classmethod
    async def close_database_connection(cls):
        """Fecha a conexão com o MongoDB."""
        if cls.client is not None:
            cls.client.close()
            cls.client = None
            print("Conexão com MongoDB fechada.")

    @classmethod
    def get_database(cls):
        """Retorna a instância do banco de dados."""
        return cls.client[settings.MONGODB_DATABASE]