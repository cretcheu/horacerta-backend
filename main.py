# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from hora_certa_app.routes import example, auth  # importamos o novo auth

app = FastAPI()

# 1) CORS: ajuste as URLs para os seus domínios
origins = [
    "http://localhost:3000",
    "https://horacerta-frontend-nb83-7gvph7pq7-cretcheus-projects.vercel.app",
    "https://horacerta-frontend-nb83-i4np2f9vc-cretcheus-projects.vercel.app",
    "https://horacerta.eu",
    "https://www.horacerta.eu",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2) Routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(example.router, prefix="/example", tags=["example"])

@app.get("/")
def root():
    return {"message": "Hora Certa Backend API online"}