import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# ====================================================================
# 1) Garanta que o diretório raiz do seu projeto esteja no Python path
# ====================================================================
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# carrega variáveis de ambiente de .env (local) ou do Railway
load_dotenv()

# importe sua Base e os módulos de modelo para o Alembic reconhecer o metadata
from hora_certa_app.db import Base
import hora_certa_app.models.user
import hora_certa_app.models.appointment

# this is the Alembic Config object, que fornece
# acesso às configurações no alembic.ini
config = context.config

# Override da URL de conexão usando a variável de ambiente
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

# Configura logging segundo o alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# metadata dos seus modelos, usado para autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations em modo 'offline'."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations em modo 'online'."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()