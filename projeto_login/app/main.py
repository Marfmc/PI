from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import get_db
from app.api import auth, services, proposals
import logging

app = FastAPI(title="Projeto Login Escalável")

# --- 2. CONFIGURAÇÃO DE CORS (PERMISSÃO PARA ACESSO EXTERNO) ---
# O "*" significa "Liberar Geral".
# Isso permite que ngrok, localhost, celular ou qualquer origem acesse sua API.
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],     # Permite GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],     # Permite enviar Tokens e Cookies
)
# ---------------------------------------------------------------

# 3. Inclui as rotas da API (Login, Cadastro, Auth)
app.include_router(auth.router, tags=["Auth"])

# Rotas de Serviços
# prefix="/services" significa que todas as URLs começarão com /services
# Ex: /services/feed, /services/my-requests
app.include_router(services.router, prefix="/services", tags=["Services"])

app.include_router(proposals.router, prefix="/proposals", tags=["Proposals"])

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
        logging.error("Database connection test failed", exc_info=True)
        return {"status": "erro", "detalhes": "Falha ao conectar ao banco de dados."}

# 4. Montar arquivos estáticos na raiz
# Isso faz com que ao acessar http://localhost:8000/, ele abra o index.html
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")