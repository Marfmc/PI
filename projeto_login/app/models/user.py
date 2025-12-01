from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)

    # --- NOVOS CAMPOS LGPD ---
    terms_accepted = Column(Boolean, default=False, nullable=False)
    accepted_at = Column(DateTime(timezone=True), server_default=func.now())

    # --- NOVOS CAMPOS PARA LÓGICA DE PAPÉIS ---
    # Indica se o usuário preencheu os dados obrigatórios de cada perfil
    is_provider_setup = Column(Boolean, default=False)   # Perfil Prestador completo?
    is_contractor_setup = Column(Boolean, default=False) # Perfil Contratante completo?