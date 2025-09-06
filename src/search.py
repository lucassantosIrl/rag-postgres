import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_postgres.vectorstores import PGVector
from typing import List, Tuple

load_dotenv()


class SemanticSearch:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small", openai_api_key=os.getenv("OPENAI_API_KEY")
        )

        self.llm = ChatOpenAI(
            model="gpt-4o-mini",  # Using gpt-4o-mini instead of gpt-5-nano as it's more available
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0,
        )

        self.connection_string = os.getenv("PGVECTOR_CONNECTION_STRING")

        try:
            self.vector_store = PGVector(
                embeddings=self.embeddings,
                connection=self.connection_string,
                collection_name="pdf_documents",
                use_jsonb=True,
            )
        except Exception as e:
            print(f"❌ Erro ao conectar com o banco de dados: {str(e)}")
            print("Verifique se o Docker Compose está rodando: docker compose up -d")
            raise

    def search_similar_documents(
        self, query: str, k: int = 10
    ) -> List[Tuple[str, float]]:
        """
        Search for similar documents in the vector database.

        Args:
            query (str): The search query
            k (int): Number of results to return

        Returns:
            List[Tuple[str, float]]: List of (document_content, similarity_score) tuples
        """
        try:
            results = self.vector_store.similarity_search_with_score(query, k=k)
            return [(doc.page_content, score) for doc, score in results]
        except Exception as e:
            print(f"❌ Erro durante a busca: {str(e)}")
            return []

    def generate_answer(self, query: str, context_documents: List[str]) -> str:
        """
        Generate an answer based on the query and context documents.

        Args:
            query (str): The user's question
            context_documents (List[str]): List of relevant document chunks

        Returns:
            str: The generated answer
        """
        context = "\n\n".join(context_documents)

        prompt = f"""CONTEXTO:
{context}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{query}

RESPONDA A "PERGUNTA DO USUÁRIO\""""

        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            return f"❌ Erro ao gerar resposta: {str(e)}"

    def ask(self, query: str) -> str:
        """
        Ask a question and get an answer based on the ingested documents.

        Args:
            query (str): The user's question

        Returns:
            str: The answer
        """
        search_results = self.search_similar_documents(query, k=10)

        if not search_results:
            return "❌ Não foi possível encontrar documentos relevantes ou houve um erro na busca."

        context_documents = [doc_content for doc_content, _ in search_results]

        answer = self.generate_answer(query, context_documents)

        return answer


if __name__ == "__main__":
    search = SemanticSearch()

    test_query = "Qual o faturamento da empresa Alfa Agronegócio Indústria?"
    print(f"Pergunta: {test_query}")
    answer = search.ask(test_query)
    print(f"Resposta: {answer}")
