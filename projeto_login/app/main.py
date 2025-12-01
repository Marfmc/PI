from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import get_db
from app.api import auth

app = FastAPI(title="Projeto Login Escalável")

app.include_router(auth.router, tags=["Auth"])

@app.get("/")
def health_check():
    return {"status": "ok", "message": "API rodando com sucesso!"}

@app.get("/test-db")
def test_db_connection(db: Session = Depends(get_db)):
    try:
        # Tenta executar um comando simples no banco
        db.execute(text("SELECT 1"))
        return {"status": "sucesso", "db": "Conectado ao MySQL!"}
    except Exception as e:
        return {"status": "erro", "detalhes": str(e)}