# main.py

import os
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 1) Carrega variáveis de ambiente do .env (local) ou do Railway
load_dotenv()

# 2) Importa engine e Base (SQLAlchemy)
from hora_certa_app.db import engine, Base

# 3) Importa seus routers
from hora_certa_app.routes import auth, example

# 4) Cria o FastAPI
app = FastAPI(title="Hora Certa Backend API")

# 5) Configura CORS
origins = [
    "http://localhost:3000",
    "https://horacerta-frontend-nb83-7gvph7pq7-cretcheus-projects.vercel.app",
    "https://horacerta-frontend-nb83-i4np2f9vc-cretcheus-projects.vercel.app",
    "https://horacerta.eu",
    "https://www.horacerta.eu",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 6) Startup event: cria todas as tabelas que ainda não existem
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# 7) Inclui as rotas
app.include_router(auth.router,    prefix="/auth",    tags=["auth"])
app.include_router(example.router, prefix="/example", tags=["example"])

# 8) Health check
@app.get("/")
def read_root():
    return {"message": "Hora Certa Backend API online"}