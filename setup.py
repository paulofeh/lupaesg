import os
import sys
from pathlib import  Path

def create_file(filepath: str, content: str = "") -> None:
    """Create a file with given content."""
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {filepath}")

def setup_project():
    """Setup initial project structure."""
    
    # Estrutura de diretórios e arquivos
    structure = {
        "app": {
            "__init__.py": "",
            "api": {
                "__init__.py": "",
                "router.py": "from fastapi import APIRouter\n\nrouter = APIRouter()\n"
            },
            "core": {
                "__init__.py": "",
                "config.py": '''from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Ambiente
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # MongoDB
    MONGODB_URL: str
    MONGODB_DATABASE: str
    
    # APIs
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
''',
                "database.py": "# MongoDB connection configuration will go here\n"
            },
            "models": {
                "__init__.py": "",
                "company.py": "# Company models will go here\n"
            },
            "services": {
                "__init__.py": "",
                "mongodb.py": "# MongoDB service functions will go here\n"
            }
        },
        "tests": {
            "__init__.py": ""
        },
        "main.py": '''from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title="LupaESG API",
    description="API para acesso a dados ESG de empresas brasileiras",
    version="0.1.0",
    debug=settings.DEBUG
)

@app.get("/")
async def read_root():
    return {"message": "Bem-vindo à API do LupaESG"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
'''
    }

    def create_structure(base_path: str, structure: dict):
        for name, content in structure.items():
            path = os.path.join(base_path, name)
            if isinstance(content, dict):
                os.makedirs(path, exist_ok=True)
                print(f"Created directory: {path}")
                create_structure(path, content)
            else:
                create_file(path, content)

    # Criar estrutura
    create_structure(".", structure)

    print("\nProject structure created successfully!")
    print("\nNext steps:")
    print("1. Run 'poetry add pydantic-settings'")
    print("2. Run 'poetry run uvicorn main:app --reload'")
    print("3. Visit http://localhost:8000 in your browser")

if __name__ == "__main__":
    setup_project()