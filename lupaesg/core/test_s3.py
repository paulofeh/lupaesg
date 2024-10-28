import boto3
from botocore.exceptions import ClientError
from lupaesg.core.config import settings
import logging

logger = logging.getLogger(__name__)


def test_s3_connection():
    """
    Testa a conexão com AWS S3 tentando listar o conteúdo do bucket
    e criar um arquivo de teste
    """
    try:
        # Inicializa cliente S3
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        )

        # Tenta criar um arquivo de teste
        test_content = b"Teste de conexao com S3"
        s3_client.put_object(
            Bucket=settings.S3_BUCKET_NAME, Key="test/connection_test.txt", Body=test_content
        )

        # Lista objetos no bucket
        response = s3_client.list_objects_v2(Bucket=settings.S3_BUCKET_NAME, Prefix="test/")

        # Verifica se o arquivo foi criado
        if "Contents" in response:
            logger.info("Conexão com S3 estabelecida com sucesso!")
            logger.info("Arquivo de teste criado em: test/connection_test.txt")

            # Lista os objetos encontrados
            for obj in response["Contents"]:
                logger.info(f"Objeto encontrado: {obj['Key']}")

            return True

    except ClientError as e:
        logger.error(f"Erro ao conectar com S3: {str(e)}")
        return False


if __name__ == "__main__":
    # Configura logging básico
    logging.basicConfig(level=logging.INFO)

    # Testa a conexão
    success = test_s3_connection()
    if not success:
        logger.error("Falha ao testar conexão com S3")
