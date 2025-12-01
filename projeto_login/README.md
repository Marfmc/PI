


# Sistema de Login Escalável (FastAPI + Docker + MySQL)

Este projeto consiste em uma API robusta de autenticação de usuários, desenvolvida com foco em escalabilidade e segurança. O ambiente é totalmente containerizado com Docker, facilitando a execução em qualquer máquina sem necessidade de instalar dependências locais.

## 🛠 Tecnologias Utilizadas

- **Linguagem:** Python 3.10
- **Framework Web:** FastAPI (Alta performance)
- **Banco de Dados:** MySQL 8.0
- **Infraestrutura:** Docker & Docker Compose
- **ORM:** SQLAlchemy
- **Gerenciador de Migrações:** Alembic
- **Autenticação:** JWT (JSON Web Tokens)
- **Segurança:** Hash de senha com Bcrypt

---

## 📋 Pré-requisitos

A única ferramenta necessária instalada no seu computador é o **Docker** (Docker Desktop).
Não é necessário instalar Python ou MySQL localmente.

---

## 🚀 Instalação e Execução

### 1. Configurar Variáveis de Ambiente
Crie um arquivo chamado `.env` na raiz do projeto (onde está o `docker-compose.yml`) e adicione o seguinte conteúdo:

```ini
DATABASE_URL=mysql+pymysql://user:password@db:3306/app_db
SECRET_KEY=sua_chave_secreta_super_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

### 👥 Trabalho em Equipe (Configuração Inicial)

1. Clone o repositório.
2. Crie seu arquivo de configuração local:
   - Copie o arquivo `.env.example` e renomeie para `.env`.
   - Se necessário, ajuste as senhas dentro dele.
3. Suba os containers:
   `docker compose up --build`
4. Crie as tabelas no seu banco local:
   `docker compose exec web alembic upgrade head`


## Estrutura do Projeto ##

projeto_login/
├── app/
│   ├── api/          # Rotas (Endpoints) e Dependências
│   ├── core/         # Configurações (Env) e Segurança (JWT/Hash)
│   ├── db/           # Conexão com Banco de Dados
│   ├── models/       # Modelos do Banco (Tabelas SQLAlchemy)
│   ├── schemas/      # Validação de Dados (Pydantic)
│   └── main.py       # Arquivo principal
├── alembic/          # Histórico de Migrações do Banco
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env

## Subir a Aplicação ##

No terminal, dentro da pasta do projeto, execute:

docker compose up --build -d
Aguarde até o terminal exibir a mensagem: Application startup complete. A API estará rodando em: http://localhost:8000


### Configuração do Banco de Dados (Migrações) ###

O comando docker compose up sobe o servidor, mas não cria as tabelas automaticamente. Para gerenciar a estrutura do banco, utilizamos o Alembic.

Abra um novo terminal na pasta do projeto e execute os comandos abaixo conforme a necessidade:

Criar/Atualizar Tabelas (Primeira vez ou após mudanças)
Sempre que você alterar um arquivo na pasta models/ ou iniciar o projeto do zero:

### Gerar o arquivo de migração ###


docker compose exec web alembic revision --autogenerate -m "descricao da alteracao"
Aplicar a mudança no banco de dados:


docker compose exec web alembic upgrade head


### Como Testar (Documentação Interativa) ###

O FastAPI fornece uma interface visual (Swagger UI) para testar as rotas.

Acesse: http://localhost:8000/docs

Criar Usuário (Sign Up):

Vá em POST /signup.

Clique em Try it out.

Preencha o JSON com email e senha e execute.

Fazer Login (Gerar Token):

Clique no botão Authorize (canto superior direito).

Digite o email (no campo username) e a senha.

Clique em Authorize e depois Close.

O cadeado ficará fechado .

Testar Rota Protegida:

Vá na rota GET /me (no final da página).

Execute. Se estiver logado, a API retornará seus dados decodificados do Token.


### Comandos Úteis ###
Parar a aplicação: Use Ctrl+C no terminal ou:


docker compose down
Reiniciar tudo do zero (Apagar banco de dados e recriar): Caso tenha problemas com migrações conflitantes:


docker compose down -v
docker compose up --build
(Lembre-se de rodar o alembic upgrade head novamente após esse comando).

## Sobre alterações nas tabelas ##

Quando mudamos o modelo, precisamos rodar a migração do Alembic. No terminal:

docker compose exec web alembic revision --autogenerate -m "add lgpd and roles"

docker compose exec web alembic upgrade head

## Subtituição de credenciais ##

acho importante deixar claro ao dev que estiver usando esse projeto que ele deve criar um arquivo .env na raiz do projeto e copiar e modificar o arquivo .env.example

falando mais sobre o uso do projeto, acho que já citei mas o dev precisa usar o comando "alembic upgrade head" para gerar o arquivo mysql_data e guardar tudo que precisa 