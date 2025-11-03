from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal
from datetime import datetime
from app.db.models import StatusProcessamento

# Schema para validação da resposta da IA
class NotaFiscalIAExtract(BaseModel):
    nome_prestador: Optional[str] = None
    cnpj_prestador: Optional[str] = None
    valor_total: Optional[Decimal] = None
    codigo_servico: Optional[str] = None
    cnae: Optional[str] = None
    tem_retencao_impostos: bool = False
    detalhes_retencao: Optional[str] = None
    data_emissao: Optional[datetime] = None # Bônus se a IA conseguir

# Schema para resposta da API (o que o Frontend vê)
class NotaFiscalResponse(BaseModel):
    id: int
    nome_prestador: Optional[str]
    cnpj_prestador: Optional[str]
    valor_total: Optional[Decimal]
    codigo_servico: Optional[str]
    status_processamento: StatusProcessamento
    tem_retencao_impostos: bool

    class Config:
        orm_mode = True # Antigo 'orm_mode', agora 'from_attributes'
        from_attributes = True

class PaginatedNotaFiscalResponse(BaseModel):
    total: int
    items: List[NotaFiscalResponse]