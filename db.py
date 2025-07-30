# hora_certa_app/db.py

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# carrega .env (se existir) para pegar um eventual DATABASE_URL
load_dotenv()

# se não tivermos DATABASE_URL, cai para SQLite local
DATABASE_URL = os.getenv("DATABASE_URL") or "sqlite:///./hora_certa_app.db"

# cria engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    echo=True,
    future=True
)

# session factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

# base declarativa
Base = declarative_base()