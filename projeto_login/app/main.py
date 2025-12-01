from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import get_db
from app.api import auth

app = FastAPI(title="Projeto Login Escalável")

# 1. Inclui as rotas da API (Login, Cadastro, Auth)
# É importante que elas venham ANTES dos arquivos estáticos
app.include_router(auth.router, tags=["Auth"])

# Rota simples de teste de saúde da API
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API rodando com sucesso!"}

# Rota de teste do banco de dados
@app.get("/test-db")
def test_db_connection(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "sucesso", "db": "Conectado ao MySQL!"}
    except Exception as e:
        return {"status": "erro", "detalhes": str(e)}

# 2. Montar arquivos estáticos na raiz
# Isso faz com que ao acessar http://localhost:8000/, ele abra o index.html
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")