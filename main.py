from fastapi import FastAPI
from hora_certa_app.routes import example

app = FastAPI()
app.include_router(example.router)

@app.get("/")
def root():
    return {"message": "Hora Certa Backend API online"}
