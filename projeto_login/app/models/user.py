from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, ForeignKey, Float, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.db.base import Base

# --- ENUMS (Para padronizar os Status) ---
class RequestStatus(str, enum.Enum):
    OPEN = "open"           # Aberto para propostas
    IN_PROGRESS = "in_progress" # Em andamento (Prestador escolhido)
    COMPLETED = "completed" # Concluído
    CANCELLED = "cancelled" # Cancelado

class ProposalStatus(str, enum.Enum):
    PENDING = "pending"     # Enviada
    ACCEPTED = "accepted"   # Contratante aceitou
    REJECTED = "rejected"   # Contratante recusou

# --- MODELO DE USUÁRIO (O que você já tinha) ---
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    
    # LGPD
    terms_accepted = Column(Boolean, default=False, nullable=False)
    accepted_at = Column(DateTime(timezone=True), server_default=func.now())

    # Flags
    is_provider_setup = Column(Boolean, default=False)
    is_contractor_setup = Column(Boolean, default=False)

    # Perfil
    full_name = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    document_id = Column(String(50), nullable=True)
    profession = Column(JSON, nullable=True) 
    bio = Column(Text, nullable=True)

    # Relacionamentos (O SQLAlchemy conecta as tabelas aqui)
    addresses = relationship("Address", back_populates="user")
    requests = relationship("ServiceRequest", back_populates="contractor") # Pedidos que eu fiz
    proposals = relationship("Proposal", back_populates="provider")       # Propostas que eu enviei

# --- NOVO: ENDEREÇOS ---
class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id")) # Pertence a quem?
    
    zip_code = Column(String(20), nullable=False) # CEP
    street = Column(String(255), nullable=False)  # Rua
    number = Column(String(20), nullable=False)   # Número
    complement = Column(String(100), nullable=True)
    neighborhood = Column(String(100), nullable=False) # Bairro
    city = Column(String(100), nullable=False)
    state = Column(String(2), nullable=False)     # UF (SP, RJ...)

    user = relationship("User", back_populates="addresses")

# --- NOVO: PEDIDOS DE SERVIÇO (A "Vaga") ---

class ServiceRequest(Base):
    __tablename__ = "service_requests"

    id = Column(Integer, primary_key=True, index=True)
    contractor_id = Column(Integer, ForeignKey("users.id"))
    
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=False)
    
    # --- NOVOS CAMPOS DE ENDEREÇO ---
    zip_code = Column(String(20), nullable=True)
    street = Column(String(255), nullable=True)
    number = Column(String(20), nullable=True)
    neighborhood = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(2), nullable=True)
    # -------------------------------
    
    status = Column(Enum(RequestStatus), default=RequestStatus.OPEN)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    contractor = relationship("User", back_populates="requests")
    proposals = relationship("Proposal", back_populates="request")

# --- NOVO: PROPOSTAS (O "Orçamento") ---
class Proposal(Base):
    __tablename__ = "proposals"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("service_requests.id")) # Para qual pedido?
    provider_id = Column(Integer, ForeignKey("users.id"))           # Quem ofereceu?
    
    price = Column(Float, nullable=False) # Valor cobrado
    description = Column(Text, nullable=True) # Detalhes ("Inclui material...")
    estimated_time = Column(String(100), nullable=True) # "2 dias"
    
    status = Column(Enum(ProposalStatus), default=ProposalStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    request = relationship("ServiceRequest", back_populates="proposals")
    provider = relationship("User", back_populates="proposals")
