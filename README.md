# PDF Semantic Search with PostgreSQL + pgVector

Sistema de ingestão e busca semântica em documentos PDF usando PostgreSQL com extensão pgVector, LangChain e OpenAI.

## 🚀 Funcionalidades

- **Ingestão de PDF**: Carrega documentos PDF, divide em chunks e armazena embeddings no PostgreSQL
- **Busca Semântica**: Realiza buscas por similaridade usando embeddings
- **Interface CLI**: Chat interativo via linha de comando
- **Respostas Contextuais**: Respostas baseadas exclusivamente no conteúdo do PDF

## 📋 Pré-requisitos

- Python 3.8+
- Docker e Docker Compose
- Chave da API OpenAI

## ⚙️ Configuração

### 1. Clone e configure o ambiente

```bash
# Navegue até o diretório do projeto
cd ingest-semantic-search-postgres

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual (Windows)
venv\Scripts\activate

# Ative o ambiente virtual (Linux/Mac)
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

### 2. Configure a chave da OpenAI

```bash
# Copie o arquivo de exemplo
copy .env.example .env

# Edite o arquivo .env e adicione sua chave da OpenAI
# OPENAI_API_KEY=sua_chave_aqui
```

### 3. Inicie o banco de dados

```bash
# Inicie o PostgreSQL com pgVector
docker compose up -d

# Verifique se está rodando
docker compose ps
```

## 🔄 Como usar

### 1. Ingestão do PDF

Coloque seu arquivo PDF na raiz do projeto com o nome `document.pdf` ou especifique o caminho:

```bash
# Usando o arquivo padrão (document.pdf)
python src/ingest.py

# Ou especificando um arquivo
python src/ingest.py caminho/para/seu/arquivo.pdf
```

### 2. Executar o chat

```bash
python src/chat.py
```

### Exemplo de uso:

```
🤖 Sistema de Busca Semântica em PDF
==================================================
Digite suas perguntas sobre o documento PDF ingerido.
Digite 'sair' ou 'exit' para encerrar.
==================================================

Faça sua pergunta:

PERGUNTA: Qual o faturamento da empresa?
RESPOSTA: O faturamento foi de 10 milhões de reais.

---

PERGUNTA: Quantos clientes temos em 2024?
RESPOSTA: Não tenho informações necessárias para responder sua pergunta.
```

## 📁 Estrutura do Projeto

```
├── docker-compose.yml     # Configuração do PostgreSQL + pgVector
├── requirements.txt       # Dependências Python
├── .env.example          # Template das variáveis de ambiente
├── src/
│   ├── ingest.py         # Script de ingestão do PDF
│   ├── search.py         # Funcionalidades de busca semântica
│   └── chat.py           # Interface CLI
├── document.pdf          # Seu arquivo PDF (adicione aqui)
└── README.md             # Este arquivo
```

## 🛠️ Tecnologias Utilizadas

- **Python**: Linguagem principal
- **LangChain**: Framework para aplicações com LLM
- **PostgreSQL + pgVector**: Banco de dados vetorial
- **OpenAI**: Embeddings (text-embedding-3-small) e LLM (gpt-4o-mini)
- **Docker**: Containerização do banco de dados

## 🔧 Configurações Técnicas

- **Chunk Size**: 1000 caracteres
- **Chunk Overlap**: 150 caracteres
- **Embeddings**: text-embedding-3-small
- **Busca**: Top 10 resultados mais similares
- **LLM**: gpt-4o-mini com temperatura 0

## ❌ Solução de Problemas

### Erro de conexão com o banco
```bash
# Verifique se o Docker está rodando
docker compose ps

# Reinicie se necessário
docker compose down
docker compose up -d
```

### Erro de API Key
- Verifique se o arquivo `.env` existe e contém a chave válida
- Teste a chave em: https://platform.openai.com/api-keys

### PDF não encontrado
- Certifique-se de que o arquivo PDF existe no caminho especificado
- Use caminhos absolutos se necessário

## 📝 Notas

- O sistema responde apenas com base no conteúdo do PDF ingerido
- Perguntas fora do contexto retornam: "Não tenho informações necessárias para responder sua pergunta."
- Para reingerir um PDF, execute novamente o script `ingest.py`
# rag-postgres
