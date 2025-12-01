from pydantic import BaseModel, EmailStr

# Base comum (dados compartilhados)
class UserBase(BaseModel):
    email: EmailStr

# Schema para criar conta (recebe senha)
class UserCreate(UserBase):
    password: str

# Schema para leitura (devolve o dado SEM a senha)
class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True