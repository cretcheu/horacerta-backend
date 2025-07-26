# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from hora_certa_app.routes import example, auth

app = FastAPI()

# Durante o teste, libere CORS para *todas* as origens
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # atenção ao wildcard aqui
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(example.router, prefix="/example", tags=["example"])

@app.get("/")
def root():
    return {"message": "Hora Certa Backend API online"}