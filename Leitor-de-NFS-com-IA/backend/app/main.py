import sys
import os

# --- CORREÇÃO DE PATH ---
# Adiciona o diretório /app (o 'WORKDIR' do Docker) ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# ---------------------

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes import api_router # Esta linha agora vai funcionar
from app.db.database import Base, engine
# ... (resto do seu código)


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes import api_router
from app.db.database import Base, engine

# Não precisamos de criar as tabelas aqui, o Alembic trata disso.
# Base.metadata.create_all(bind=engine) 

app = FastAPI(title="NF-Extractor API")

# --- Configuração do CORS ---
# Permite que o Frontend (ex: localhost:3000) acesse o Backend (ex: localhost:8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Em produção, mude para: ["http://localhost:3000", "http://seu-dominio.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Rotas da API ---
app.include_router(api_router, prefix="/api/v1")

@app.get("/health", tags=["Health Check"])
def health_check():
    return {"status": "ok"} 