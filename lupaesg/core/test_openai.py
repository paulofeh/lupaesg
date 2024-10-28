from openai import OpenAI
from lupaesg.core.config import settings
import logging
import numpy as np
from typing import Dict, Any

logger = logging.getLogger(__name__)


def test_openai_connection() -> Dict[str, Any]:
    """
    Testa a conexão com OpenAI API gerando um embedding de teste
    e retornando informações sobre o resultado
    """
    try:
        # Inicializa cliente OpenAI
        client = OpenAI(api_key=settings.OPENAI_API_KEY)

        # Texto de teste - um pequeno trecho relacionado a ESG
        test_text = """
        A empresa mantém programa de gestão ambiental e possui certificação ISO 14001.
        Em 2023, reduziu suas emissões de CO2 em 15% através de iniciativas de eficiência energética.
        """

        # Gera embedding
        response = client.embeddings.create(
            model=settings.OPENAI_MODEL, input=test_text, encoding_format="float"
        )

        # Extrai o embedding
        embedding = response.data[0].embedding

        # Análise básica do embedding
        embedding_array = np.array(embedding)

        info = {
            "dimensoes": len(embedding),
            "media": float(np.mean(embedding_array)),
            "desvio_padrao": float(np.std(embedding_array)),
            "min": float(np.min(embedding_array)),
            "max": float(np.max(embedding_array)),
        }

        # Loga informações
        logger.info("Conexão com OpenAI API estabelecida com sucesso!")
        logger.info(f"Modelo utilizado: {settings.OPENAI_MODEL}")
        logger.info(f"Dimensões do embedding: {info['dimensoes']}")
        logger.info(f"Média dos valores: {info['media']:.6f}")
        logger.info(f"Desvio padrão: {info['desvio_padrao']:.6f}")

        return info

    except Exception as e:
        logger.error(f"Erro ao conectar com OpenAI API: {str(e)}")
        raise


if __name__ == "__main__":
    # Configura logging básico
    logging.basicConfig(level=logging.INFO)

    try:
        # Testa a conexão
        info = test_openai_connection()
        logger.info("Teste concluído com sucesso!")
    except Exception as e:
        logger.error("Falha ao testar conexão com OpenAI API")
        logger.error(str(e))
