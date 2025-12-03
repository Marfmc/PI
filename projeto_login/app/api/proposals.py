from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.user import User, Proposal, ServiceRequest, ProposalStatus
from app.schemas.proposal import ProposalCreate, ProposalResponse
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=ProposalResponse)
def create_proposal(
    proposal: ProposalCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 1. Segurança: Só prestador com perfil completo pode enviar proposta
    if not current_user.is_provider_setup:
        raise HTTPException(status_code=400, detail="Você precisa completar seu perfil de prestador.")

    # 2. Verificar se o pedido existe
    service_request = db.query(ServiceRequest).filter(ServiceRequest.id == proposal.request_id).first()
    if not service_request:
        raise HTTPException(status_code=404, detail="Pedido de serviço não encontrado.")

    # 3. Impedir proposta duplicada (Opcional, mas boa prática)
    # Verifica se esse prestador já mandou proposta para esse serviço
    existing_proposal = db.query(Proposal).filter(
        Proposal.request_id == proposal.request_id,
        Proposal.provider_id == current_user.id
    ).first()
    
    if existing_proposal:
        raise HTTPException(status_code=400, detail="Você já enviou uma proposta para este serviço.")

    # 4. Criar a Proposta
    new_proposal = Proposal(
        request_id=proposal.request_id,
        provider_id=current_user.id,
        price=proposal.price,
        description=proposal.description,
        estimated_time=proposal.estimated_time,
        status=ProposalStatus.PENDING
    )

    db.add(new_proposal)
    db.commit()
    db.refresh(new_proposal)
    
    return new_proposal

# Rota para ver as propostas que EU enviei (Histórico do Prestador)
@router.get("/my-proposals", response_model=List[ProposalResponse])
def get_my_proposals(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Proposal).filter(Proposal.provider_id == current_user.id).all()