import sys
import logging
from pathlib import Path
from datetime import datetime
from logging.handlers import RotatingFileHandler
from .config import get_settings

settings = get_settings()

# Criar diretório de logs se não existir
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Nome do arquivo de log com data
log_file = log_dir / f"lupaesg_{datetime.now().strftime('%Y%m')}.log"

# Formato do log
log_format = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def setup_logger(name: str) -> logging.Logger:
    """
    Configura e retorna um logger com o nome especificado.
    """
    logger = logging.getLogger(name)
    
    # Se o logger já foi configurado, retorna ele
    if logger.hasHandlers():
        return logger
        
    # Configura o nível base de logging baseado no ambiente
    logger.setLevel(logging.DEBUG if settings.debug else logging.INFO)
    
    # Handler para arquivo
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10485760,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(log_format)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    
    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)
    console_handler.setLevel(logging.DEBUG if settings.debug else logging.INFO)
    logger.addHandler(console_handler)
    
    # Evita propagação para loggers pai
    logger.propagate = False
    
    return logger

# Logger principal da aplicação
logger = setup_logger("lupaesg")