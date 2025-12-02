from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, ProviderSetupRequest
from app.schemas.token import Token
from app.core.security import get_password_hash, verify_password, create_access_token
from app.api.deps import get_current_user 

router = APIRouter()

# --- CADASTRO (LGPD) ---
@router.post("/signup", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if not user.terms_accepted:
        raise HTTPException(status_code=400, detail="É necessário aceitar os termos de uso.")

    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email já registrado")
    
    hashed_password = get_password_hash(user.password)
    
    new_user = User(
        email=user.email, 
        hashed_password=hashed_password,
        terms_accepted=user.terms_accepted,
        is_provider_setup=False,
        is_contractor_setup=False
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

# --- LOGIN ---
@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# --- ROTA DE PERFIL ---
@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# --- ROTA DELETAR CONTA (LGPD) ---
@router.delete("/me", status_code=204)
def delete_my_account(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db.delete(current_user)
    db.commit()
    return

# --- ROTA: ATIVAR PRESTADOR (Aqui estava o problema provável) ---
@router.put("/me/setup_provider")
def setup_provider_profile(
    data: ProviderSetupRequest, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    current_user.full_name = data.full_name
    current_user.phone = data.phone
    current_user.document_id = data.document_id
    current_user.profession = data.profession
    current_user.bio = data.bio
    
    current_user.is_provider_setup = True
    
    db.commit()
    db.refresh(current_user)
    
    return {"message": "Perfil de prestador ativado com sucesso!"}