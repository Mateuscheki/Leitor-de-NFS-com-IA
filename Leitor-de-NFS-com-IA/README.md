NF-Extractor 📄

NF-Extractor é uma aplicação web full-stack projetada para automatizar a extração de dados de Notas Fiscais (NFs) brasileiras. Faça o upload de um PDF ou imagem, e o sistema usará OCR (Tesseract) para analisar o documento, extrair informações-chave (Prestador, CNPJ, Valor, etc.) e salvá-las em um banco de dados, exibindo tudo em um dashboard amigável.

🚀 Tecnologias Utilizadas

Este projeto é construído com um stack de tecnologias moderno e containerizado:

Backend: FastAPI (Python 3.11)

Frontend: React (com Material-UI)

Banco de Dados: MySQL 8.0

Extração de Texto (OCR): Tesseract

Manipulação de PDF: Poppler

Containerização: Docker e Docker Compose

Migrações de DB: Alembic

Gerenciamento de DB: PhpMyAdmin (para depuração)

📋 Pré-requisitos

Antes de começar, garanta que você tenha as seguintes ferramentas instaladas em sua máquina:

Docker

Docker Compose (geralmente já incluído no Docker Desktop)

⚡ Como Iniciar o Projeto

Siga estes passos para configurar e iniciar toda a aplicação localmente.

1. Clone o Repositório

git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
cd seu-repositorio


2. Crie o Arquivo de Ambiente do Backend

O backend precisa de um arquivo .env para armazenar as chaves da API e a URL do banco de dados.

Navegue até a pasta backend:

cd backend


Crie um arquivo chamado .env:

touch .env


Abra o arquivo .env e cole o seguinte conteúdo (substitua a chave da OpenAI se estiver usando):

# URL de conexão que o Alembic e o FastAPI usarão
# (Note: 'db-mysql' é o nome do serviço no docker-compose.yml)
DATABASE_URL=mysql+pymysql://user:password@db-mysql:3306/nf_extractor_db

# Chave da API da OpenAI (se o seu ai_service.py a utilizar)
OPENAI_API_KEY=sk-sua-chave-aqui


Volte para o diretório raiz do projeto:

cd ..


3. Crie as Dependências Faltantes (Alembic)

O Alembic precisa de alguns arquivos e pastas que podem não estar no Git. Crie-os manually:

# 1. Crie a pasta para os scripts de migração
mkdir -p backend/alembic/versions

# 2. Crie o template de script (copie o conteúdo abaixo)
touch backend/alembic/script.py.mako


Cole este conteúdo no arquivo backend/alembic/script.py.mako:

"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | repr}
Create Date: ${create_date}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}


4. Adicione a Dependência de Criptografia

O MySQL 8.0 requer um pacote Python extra para autenticação.

Abra o arquivo backend/requirements.txt.

Adicione a seguinte linha no final:

cryptography


5. Inicie os Contêineres

Agora você está pronto para iniciar tudo. Este comando irá construir as imagens (instalando o cryptography) e iniciar todos os serviços.

docker-compose up --build -d


(O -d inicia os contêineres em modo "detached" (em segundo plano).)

⚠️ Troubleshooting: Criando as Tabelas (Migração Inicial)

Ao iniciar pela primeira vez, o comando alembic upgrade head no CMD do Docker pode falhar porque o script de migração inicial ainda não foi gerado.

Se você tentar fazer um upload e receber um erro Table 'notas_fiscais' doesn't exist, siga estes passos:

Entre no contêiner do backend:

docker-compose exec backend /bin/sh


Gere o script de migração (o Alembic irá comparar seus models.py com o banco vazio):

DATABASE_URL="mysql+pymysql://user:password@db-mysql:3306/nf_extractor_db" alembic revision --autogenerate -m "Cria tabelas iniciais"


(Você verá uma saída ... done)

Aplique o script de migração (isto irá criar as tabelas):

DATABASE_URL="mysql+pymysql://user:password@db-mysql:3306/nf_extractor_db" alembic upgrade head


(Você verá uma saída INFO [alembic.runtime.migration] Running upgrade...)

Saia do contêiner:

exit


Suas tabelas agora existem e a aplicação está pronta para uso.

🖥️ Acessando a Aplicação

Aplicação (Frontend): http://localhost (ou http://localhost:80)

Documentação da API (Swagger): http://localhost:8000/docs

Gerenciador do Banco (PhpMyAdmin): http://localhost:8080


Login: root / rootpassword

.env
DATABASE_URL=mysql+pymysql://user:password@db-mysql:3306/nf_extractor_db
OPENAI_API_KEY="sk-..."

