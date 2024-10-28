from lupaesg.core.mongodb import get_mongodb
from lupaesg.core.logging import setup_logger

logger = setup_logger("test_mongodb")

def test_connection():
    mongodb = None
    try:
        logger.info("Iniciando teste de conexão com MongoDB")
        
        # Obtém a instância do MongoDB
        mongodb = get_mongodb()
        db = mongodb.db
        
        # Tenta uma operação simples
        logger.debug("Tentando inserir documento de teste")
        db.test_collection.insert_one({"test": "Hello MongoDB!"})
        result = db.test_collection.find_one({"test": "Hello MongoDB!"})
        
        logger.info("✅ Conexão com MongoDB estabelecida com sucesso!")
        logger.debug("Documento inserido: %s", result)
        
        # Limpa o documento de teste
        logger.debug("Removendo documento de teste")
        db.test_collection.delete_one({"test": "Hello MongoDB!"})
        
    except Exception as e:
        logger.error("❌ Erro ao conectar com MongoDB: %s", str(e))
        raise
    finally:
        if mongodb:
            mongodb.close()

if __name__ == "__main__":
    test_connection()