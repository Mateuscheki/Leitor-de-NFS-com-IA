import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# --- CORREÇÃO DE PATH ---
# Adiciona o diretório 'app' (um nível acima) ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# ---------------------

# --- IMPORTAÇÕES PRINCIPAIS ---
# Importe o Base do seu arquivo de database
from app.db.database import Base

# Importe suas settings (para pegar a DATABASE_URL)
from app.core.settings import settings

# --- LINHA CRÍTICA ---
# Esta linha importa seus modelos (ex: models.py) e os "registra"
# no Base.metadata. Sem ela, o Alembic acha que o banco está vazio.
import app.db.models
# ---------------------------

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
# --- CORREÇÃO DO LOGGING (KeyError: 'formatters') ---
# Comentamos a linha abaixo pois o alembic.ini não tem a seção [formatters]
if config.config_file_name is not None:
    # fileConfig(config.config_file_name)
    pass # Adicionamos 'pass' para o 'if' não ficar vazio
# ---------------------------------------------------

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.
    """
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.
    """
    
    # --- CORREÇÃO DO AttributeError ---
    # Usamos a URL das settings e o nome da seção correto
    
    # Pega a seção de configuração do alembic.ini (o nome correto é config_ini_section)
    section = config.get_section(config.config_ini_section, {})
    
    # Sobrescreve a URL do .ini com a URL das nossas settings
    section['sqlalchemy.url'] = settings.DATABASE_URL
    
    connectable = engine_from_config(
        section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()