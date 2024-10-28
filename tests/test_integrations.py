from openai import OpenAI
from pinecone import Pinecone
from lupaesg.core.config import settings
import logging
import time
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class EmbeddingService:
    """
    Serviço para testar a integração entre OpenAI e Pinecone
    """
    def __init__(self):
        # Inicializa cliente OpenAI
        self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Inicializa Pinecone
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        
        # Conecta ao índice
        self.index = self.pc.Index(settings.PINECONE_INDEX_NAME)
        
    def generate_embedding(self, text: str) -> List[float]:
        """Gera embedding usando OpenAI"""
        response = self.openai_client.embeddings.create(
            model=settings.OPENAI_MODEL,
            input=text,
            encoding_format="float"
        )
        return response.data[0].embedding
    
    def test_integration(self) -> Dict[str, Any]:
        """Testa o fluxo completo: geração de embedding, upsert e busca"""
        try:
            # Textos de teste
            texts = {
                "ambiental": """
                A empresa mantém programa de gestão ambiental e possui certificação ISO 14001.
                Em 2023, reduziu suas emissões de CO2 em 15% através de iniciativas de eficiência energética.
                """,
                "social": """
                O programa de diversidade e inclusão da empresa resultou em 45% de mulheres em cargos de liderança.
                Foram investidos R$ 2 milhões em projetos sociais nas comunidades do entorno.
                """,
                "governanca": """
                O Conselho de Administração é composto por 30% de membros independentes.
                A empresa possui política de compliance robusta e canal de denúncias terceirizado.
                """
            }
            
            # Gera embeddings e insere no Pinecone
            for category, text in texts.items():
                embedding = self.generate_embedding(text)
                
                # Insere no Pinecone
                self.index.upsert(
                    vectors=[
                        {
                            "id": f"test_{category}",
                            "values": embedding,
                            "metadata": {"category": category, "text": text}
                        }
                    ]
                )
                logger.info(f"Inserido embedding da categoria: {category}")
                
                # Pequena pausa para não sobrecarregar as APIs
                time.sleep(1)
            
            # Faz uma busca de similaridade
            query_text = "Quais são as práticas ambientais da empresa?"
            query_embedding = self.generate_embedding(query_text)
            
            search_results = self.index.query(
                vector=query_embedding,
                top_k=3,
                include_metadata=True
            )
            
            # Processa resultados
            results = []
            for match in search_results['matches']:
                results.append({
                    "category": match.metadata["category"],
                    "score": match.score,
                    "text": match.metadata["text"]
                })
            
            return {
                "status": "success",
                "query": query_text,
                "results": results
            }
            
        except Exception as e:
            logger.error(f"Erro durante o teste: {str(e)}")
            raise

def main():
    """Função principal de teste"""
    logging.basicConfig(level=logging.INFO)
    
    try:
        service = EmbeddingService()
        logger.info("Iniciando teste de integração OpenAI + Pinecone...")
        
        results = service.test_integration()
        
        logger.info("\nResultados da busca:")
        logger.info(f"Query: {results['query']}\n")
        
        for idx, result in enumerate(results['results'], 1):
            logger.info(f"Resultado {idx}:")
            logger.info(f"Categoria: {result['category']}")
            logger.info(f"Score de similaridade: {result['score']:.4f}")
            logger.info(f"Texto: {result['text']}\n")
            
    except Exception as e:
        logger.error("Falha no teste de integração")
        logger.error(str(e))

if __name__ == "__main__":
    main()