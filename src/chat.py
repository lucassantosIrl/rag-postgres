#!/usr/bin/env python3
"""
CLI Chat Interface for PDF Semantic Search
"""

import os
import sys
from dotenv import load_dotenv
from search import SemanticSearch

load_dotenv()

print(os.getenv("PGVECTOR_CONNECTION_STRING"))


def main():
    print("🤖 Sistema de Busca Semântica em PDF")
    print("=" * 50)
    print("Digite suas perguntas sobre o documento PDF ingerido.")
    print("Digite 'sair' ou 'exit' para encerrar.")
    print("=" * 50)

    if not os.getenv("OPENAI_API_KEY"):
        print("Erro: OPENAI_API_KEY não encontrada!")
        print(
            "Crie um arquivo .env baseado no .env.example e configure sua chave da OpenAI."
        )
        sys.exit(1)

    try:
        print("Inicializando sistema de busca...")
        search = SemanticSearch()
        print("Sistema inicializado com sucesso!")
        print()
    except Exception as e:
        print(f"Erro ao inicializar o sistema: {str(e)}")
        print("Verifique se:")
        print("1. O Docker Compose está rodando: docker compose up -d")
        print("2. O PDF foi ingerido: python src/ingest.py")
        print("3. A variável OPENAI_API_KEY está configurada")
        sys.exit(1)

    while True:
        try:
            print("Faça sua pergunta:")
            question = input("\nPERGUNTA: ").strip()

            if question.lower() in ["sair", "exit", "quit", "q"]:
                print("\n Até logo!")
                break

            if not question:
                print("Por favor, digite uma pergunta válida.")
                continue

            print("Processando...")
            answer = search.ask(question)

            print(f"RESPOSTA: {answer}")
            print("\n" + "-" * 50 + "\n")

        except KeyboardInterrupt:
            print("\n\n Chat interrompido pelo usuário. Até logo!")
            break
        except Exception as e:
            print(f"Erro inesperado: {str(e)}")
            print("Tente novamente ou reinicie o sistema.\n")


if __name__ == "__main__":
    main()
