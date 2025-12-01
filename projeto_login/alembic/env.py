import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# 1. Adicionar o diretório raiz ao path para conseguir importar 'app'
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# 2. Importar suas configurações e modelos
from app.core.config import settings
from app.db.base import Base
from app.models.user import User  # <--- Importante: Importar o modelo para o Alembic ver!

config = context.config
fileConfig(config.config_file_name)

# 3. Apontar o metadata para o seu Base
target_metadata = Base.metadata

# 4. Sobrescrever a URL do banco com a variável de ambiente
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata, compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()