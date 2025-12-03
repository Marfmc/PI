from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# O que chega do Frontend (Criação)
class ServiceRequestCreate(BaseModel):
    title: str
    description: str
    category: str
    zip_code: str
    street: str
    number: str
    neighborhood: str
    city: str
    state: str

# O que sai para o Frontend (Leitura)
class ServiceRequestResponse(BaseModel):
    id: int
    title: str
    description: str
    category: str
    status: str
    created_at: datetime
    contractor_id: int
    
    # Campos de Endereço
    city: Optional[str] = None
    state: Optional[str] = None
    
    # NOVO: Nome do Cliente para o Card/Modal
    contractor_name: Optional[str] = "Cliente ConstruFácil" 

    class Config:
        from_attributes = True