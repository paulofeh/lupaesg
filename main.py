from fastapi import FastAPI
from app.core.config import settings
from app.core.database import MongoDB

app = FastAPI(
    title="LupaESG API",
    description="API para acesso a dados ESG de empresas brasileiras",
    version="0.1.0",
    debug=settings.DEBUG
)

@app.on_event("startup")
async def startup_db_client():
    await MongoDB.connect_to_database()

@app.on_event("shutdown")
async def shutdown_db_client():
    await MongoDB.close_database_connection()

@app.get("/")
async def read_root():
    return {"message": "Bem-vindo à API do LupaESG"}

@app.get("/test-db")
async def test_db():
    """Rota de teste para verificar a conexão com o MongoDB."""
    try:
        db = MongoDB.get_database()
        await db.command("ping")
        return {"message": "Conexão com MongoDB estabelecida com sucesso!"}
    except Exception as e:
        return {"error": f"Erro ao conectar ao MongoDB: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)