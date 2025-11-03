import enum
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime,
    DECIMAL, Enum
)
from sqlalchemy.sql import func
from app.db.database import Base


class StatusProcessamento(str, enum.Enum):
    PENDENTE = "PENDENTE"
    PROCESSADO = "PROCESSADO"
    ERRO = "ERRO"


class NotaFiscal(Base):
    __tablename__ = "notas_fiscais"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Dados extraídos
    nome_prestador = Column(String(255), nullable=True)
    cnpj_prestador = Column(String(20), index=True, nullable=True)
    valor_total = Column(DECIMAL(10, 2), nullable=True)
    codigo_servico = Column(String(20), nullable=True)
    cnae = Column(String(20), nullable=True)
    tem_retencao_impostos = Column(Boolean, default=False)
    detalhes_retencao = Column(String(500), nullable=True)

    # Metadados do processamento
    data_emissao = Column(DateTime, nullable=True)  # A IA pode extrair isso
    status_processamento = Column(
        Enum(StatusProcessamento),
        default=StatusProcessamento.PENDENTE
    )
    texto_extraido_raw = Column(Text, nullable=True)

    # Timestamps (Bônus)
    data_upload = Column(DateTime(timezone=True), server_default=func.now())
    data_processamento = Column(DateTime(timezone=True), onupdate=func.now())