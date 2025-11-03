import os
import shutil
from typing import List, Optional
from fastapi import (
    APIRouter, Depends, UploadFile, File, HTTPException,
    BackgroundTasks, Query
)
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import models, schemas
from app.services import ocr_service, ai_service
from app.db.database import SessionLocal

router = APIRouter()

# --- Diretório de Uploads Temporários ---
UPLOAD_DIR = "/tmp/nf_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# --- Tarefa Assíncrona (Background) ---

async def processar_nota(nota_id: int, file_path: str, mime_type: str, db: Session):
    """
    Função executada em background para processar a nota fiscal.
    """
    try:
        print(f"[BG Task] Iniciando processamento da Nota ID: {nota_id}")

        # 1. Obter o registro do banco
        db_nota = db.query(models.NotaFiscal).filter(models.NotaFiscal.id == nota_id).first()
        if not db_nota:
            print(f"[BG Task] ERRO: Nota ID {nota_id} não encontrada.")
            return

        # 2. Extração de Texto (OCR)
        try:
            texto_bruto = await ocr_service.extrair_texto_de_arquivo(file_path, mime_type)
            db_nota.texto_extraido_raw = texto_bruto
            db.commit()
            print(f"[BG Task] Nota ID {nota_id}: Extração de texto concluída.")
        except Exception as e:
            raise Exception(f"Falha no OCR: {e}")

        # 3. Análise com IA (OpenAI)
        try:
            dados_extraidos = await ai_service.analisar_texto_nf(texto_bruto)
            print(f"[BG Task] Nota ID {nota_id}: Análise da IA concluída.")
        except Exception as e:
            raise Exception(f"Falha na IA: {e}")

        # 4. Atualizar o banco com os dados extraídos
        update_data = dados_extraidos.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_nota, key, value)

        db_nota.status_processamento = models.StatusProcessamento.PROCESSADO
        db.commit()
        print(f"[BG Task] Nota ID {nota_id}: Processamento CONCLUÍDO.")

    except Exception as e:
        # 5. Lidar com erros
        print(f"[BG Task] ERRO FATAL no processamento da Nota ID {nota_id}: {e}")
        if 'db_nota' in locals():
            db_nota.status_processamento = models.StatusProcessamento.ERRO
            db_nota.detalhes_retencao = f"Erro no processamento: {str(e)}"  # Reaproveitando campo
            db.commit()

    finally:
        # 6. Limpar arquivo temporário
        if os.path.exists(file_path):
            os.remove(file_path)
        print(f"[BG Task] Limpeza do arquivo {file_path} concluída.")


# --- Endpoints da API ---

@router.post("/upload", status_code=202)  # 202 Accepted (Processamento iniciado)
async def upload_nota_fiscal(
        background_tasks: BackgroundTasks,
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    """
    Endpoint de upload. Aceita o arquivo e inicia o processamento em background.
    """

    # 1. Validar tipo de arquivo
    allowed_types = ["application/pdf", "image/png", "image/jpeg"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Tipo de arquivo não suportado.")

    # 2. Salvar arquivo temporariamente
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()

    # 3. Criar registro inicial no DB
    try:
        db_nota = models.NotaFiscal(
            nome_prestador=file.filename,  # Nome temporário
            status_processamento=models.StatusProcessamento.PENDENTE
        )
        db.add(db_nota)
        db.commit()
        db.refresh(db_nota)
    except Exception as e:
        os.remove(file_path)  # Limpa o arquivo se falhar ao criar no DB
        raise HTTPException(status_code=500, detail=f"Erro ao salvar no DB: {e}")

    # 4. Adicionar a tarefa pesada (OCR + IA) ao background
    # Precisamos criar uma nova sessão de DB para a thread background
    db_session_bg = SessionLocal()

    background_tasks.add_task(
        processar_nota,
        db_nota.id,
        file_path,
        file.content_type,
        db_session_bg
    )

    return {"message": "Upload recebido. Processamento iniciado.", "nota_id": db_nota.id}


@router.get("/", response_model=schemas.PaginatedNotaFiscalResponse)
async def get_notas(
        db: Session = Depends(get_db),
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100)
):
    """
    Retorna uma lista paginada de todas as notas fiscais.
    """
    query = db.query(models.NotaFiscal).order_by(models.NotaFiscal.id.desc())

    total = query.count()
    items = query.offset(skip).limit(limit).all()

    return {"total": total, "items": items}