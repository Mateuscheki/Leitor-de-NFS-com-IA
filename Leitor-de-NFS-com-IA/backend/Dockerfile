# Estágio Base: Instala dependências do SO (Tesseract e Poppler)
FROM python:3.11-slim AS base
WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-por \  
    poppler-utils \     
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Estágio de Build: Instala dependências Python
FROM base AS build
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Estágio Final: Copia o código da aplicação
FROM base
WORKDIR /app

# Copia as libs E os executáveis (bin)
COPY --from=build /usr/local /usr/local

COPY . .

# Expõe a porta que o Uvicorn usará
EXPOSE 8000

# --- CORREÇÃO APLICADA AQUI ---
# Define o PYTHONPATH para incluir o diretório base /app
# Assim, o Python consegue encontrar o "pacote app" (em /app/app)
ENV PYTHONPATH="/app"
# -----------------------------

# Comando para iniciar o servidor (e aplicar migrações)
CMD ["sh", "-c", "alembic upgrade head && PYTHONPATH=/app python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"]