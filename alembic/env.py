import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# ─── 1) Assegura que o CWD (raiz do projeto) esteja no PYTHONPATH ──────────
# Executar "pwd" deve mostrar a pasta que contém alembic.ini e hora_certa_app/
sys.path.insert(0, os.getcwd())

# ─── 2) Carrega .env local (ou ignore se usar só env vars do Railway) ──────
load_dotenv(os.path.join(os.getcwd(), ".env"))

# ─── 3) Importe Base e modelos para que o Alembic “autogenerate” funcione ──
from hora_certa_app.db import Base
import hora_certa_app.models.user
import hora_certa_app.models.appointment

# ─── 4) Configura o Alembic com a URL do env var ──────────────────────────
config = context.config
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

# logging conforme definido no alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# metadata dos seus modelos
target_metadata = Base.metadata

# ─── 5) Funções de migração offline/online ─────────────────────────────────
def run_migrations_offline() -> None:
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
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


# ─── 6) Execução conforme o modo ────────────────────────────────────────────
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()