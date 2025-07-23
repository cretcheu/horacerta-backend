# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from hora_certa_app.routes import example, auth

app = FastAPI()

# CORS usando regex para aceitar *qualquer* subdomínio/vercel preview
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://horacerta-frontend-nb83-.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(example.router, prefix="/example", tags=["example"])

@app.get("/")
def root():
    return {"message": "Hora Certa Backend API online"}