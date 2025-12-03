from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# O que o Prestador envia
class ProposalCreate(BaseModel):
    request_id: int       # ID do pedido que ele quer pegar
    price: float          # Valor (R$)
    description: str      # Detalhes ("Inclui material", etc)
    estimated_time: str   # Ex: "2 dias", "1 semana"

# O que o sistema devolve
class ProposalResponse(BaseModel):
    id: int
    request_id: int
    provider_id: int
    price: float
    description: str
    estimated_time: str
    status: str           # PENDING, ACCEPTED, REJECTED
    created_at: datetime

    class Config:
        from_attributes = True