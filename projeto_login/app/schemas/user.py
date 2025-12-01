from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    terms_accepted: bool # <--- Novo campo obrigatório no cadastro

class UserResponse(UserBase):
    id: int
    is_active: bool
    terms_accepted: bool
    accepted_at: Optional[datetime]
    is_provider_setup: bool   # O front precisa saber disso para redirecionar
    is_contractor_setup: bool # O front precisa saber disso para redirecionar

    class Config:
        from_attributes = True