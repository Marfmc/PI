from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.db.session import get_db
from app.models.user import User, ServiceRequest, RequestStatus
from app.schemas.service import ServiceRequestCreate, ServiceRequestResponse
from app.api.deps import get_current_user

router = APIRouter()

# --- 1. CRIAR PEDIDO ---
@router.post("/", response_model=ServiceRequestResponse)
def create_service_request(
    request: ServiceRequestCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_request = ServiceRequest(
        title=request.title,
        description=request.description,
        category=request.category,
        contractor_id=current_user.id,
        status=RequestStatus.OPEN,
        
        # Endereço
        zip_code=request.zip_code,
        street=request.street,
        number=request.number,
        neighborhood=request.neighborhood,
        city=request.city,
        state=request.state
    )

    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request

# --- 2. LISTAR PEDIDOS (FEED) - COM NOME DO CLIENTE ---
@router.get("/feed", response_model=List[ServiceRequestResponse])
def get_service_feed(
    category: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # joinedload: Traz os dados do usuário (contractor) junto com o pedido para ser rápido
    query = db.query(ServiceRequest).options(joinedload(ServiceRequest.contractor)).filter(ServiceRequest.status == RequestStatus.OPEN)
    
    if category:
        query = query.filter(ServiceRequest.category == category)
        
    results = query.order_by(ServiceRequest.created_at.desc()).all()

    # Preenche o nome do cliente manualmente antes de enviar
    feed_data = []
    for req in results:
        # Converte o objeto do banco para o Schema Pydantic
        item = ServiceRequestResponse.model_validate(req)
        
        # Lógica para decidir qual nome mostrar
        if req.contractor:
            if req.contractor.full_name:
                item.contractor_name = req.contractor.full_name
            else:
                # Se não tiver nome completo, pega a primeira parte do email
                item.contractor_name = req.contractor.email.split('@')[0]
        
        feed_data.append(item)
        
    return feed_data

# --- 3. MEUS PEDIDOS ---
@router.get("/my-requests", response_model=List[ServiceRequestResponse])
def get_my_requests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(ServiceRequest).filter(
        ServiceRequest.contractor_id == current_user.id
    ).order_by(ServiceRequest.created_at.desc()).all()