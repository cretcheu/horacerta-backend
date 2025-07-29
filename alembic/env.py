import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# ─────────────────────────────────────────────────────────────────────────────
# 1) Ajuste do path: garante que "hora_certa_app" (o package) seja importável
# ─────────────────────────────────────────────────────────────────────────────
# insere o diretório-pai de alembic/ em sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# ─────────────────────────────────────────────────────────────────────────────
# 2) Carregamento de variáveis de ambiente (se usar .env local)
# ─────────────────────────────────────────────────────────────────────────────
load_dotenv()

# ─────────────────────────────────────────────────────────────────────────────
# 3) Import dos seus modelos e Base
# ─────────────────────────────────────────────────────────────────────────────
from hora_certa_app.db import Base
import hora_certa_app.models.user
import hora_certa_app.models.appointment

# ─────────────────────────────────────────────────────────────────────────────
# 4) Configurações do Alembic
# ─────────────────────────────────────────────────────────────────────────────
config = context.config

# Override da URL de conexão para usar a env var
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

# Logging conforme definido no alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata dos modelos — usado no autogenerate
target_metadata = Base.metadata

# ─────────────────────────────────────────────────────────────────────────────
# 5) Funções de migração offline e online
# ─────────────────────────────────────────────────────────────────────────────
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


# ─────────────────────────────────────────────────────────────────────────────
# 6) Entry point: escolhe offline ou online
# ─────────────────────────────────────────────────────────────────────────────
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()