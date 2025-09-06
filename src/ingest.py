import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_postgres.vectorstores import PGVector

# Load environment variables
load_dotenv()

print(os.getenv("PGVECTOR_CONNECTION_STRING"))


def ingest_pdf(pdf_path: str):
    """
    Ingest a PDF file into the PostgreSQL vector database.

    Args:
        pdf_path (str): Path to the PDF file to ingest
    """

    CONNECTION_STRING = os.getenv("PGVECTOR_CONNECTION_STRING")

    VECTOR_SIZE = 1000

    print(f"Iniciando ingestão do PDF: {pdf_path}")

    if not os.path.exists(pdf_path):
        print(f"Erro: Arquivo PDF não encontrado: {pdf_path}")
        return

    print("Carregando PDF...")
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    print(f"PDF carregado com {len(documents)} páginas")

    print("Dividindo documento em chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=VECTOR_SIZE, chunk_overlap=150
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Documento dividido em {len(chunks)} chunks")

    print("Inicializando embeddings OpenAI...")
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    print("Criando embeddings e salvando no banco de dados...")
    try:
        # Initialize vectorstore according to documentation
        vectorstore = PGVector(
            embeddings=embeddings,
            collection_name="pdf_documents",
            connection=CONNECTION_STRING,
            use_jsonb=True,
        )

        # Add documents to the vectorstore
        vectorstore.add_documents(chunks)

        print(
            f"✅ Ingestão concluída! {len(chunks)} chunks foram salvos no banco de dados."
        )

    except Exception as e:
        print(f"❌ Erro durante a ingestão: {str(e)}")
        print("Verifique se:")
        print("1. O Docker Compose está rodando (docker compose up -d)")
        print("2. A variável OPENAI_API_KEY está configurada no arquivo .env")
        print("3. A conexão com o PostgreSQL está funcionando")


if __name__ == "__main__":
    pdf_path = "document.pdf"

    import sys

    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]

    ingest_pdf(pdf_path)
