# hora_certa_app/routes/auth.py

from typing import Optional
from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import jwt

# Configurações de JWT
SECRET_KEY = "sua_chave_secreta_aqui"  # Troque por algo seguro em produção
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()

# Schemas
class RegisterIn(BaseModel):
    name: str
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

# “Banco” temporário em memória
fake_users_db: dict[str, dict] = {}

# Funções utilitárias
def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Rotas
@router.post("/register", response_model=TokenOut)
async def register(input: RegisterIn):
    if input.email in fake_users_db:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    hashed = get_password_hash(input.password)
    fake_users_db[input.email] = {
        "name": input.name,
        "hashed_password": hashed
    }
    token = create_access_token({"sub": input.email})
    return {"access_token": token}

@router.post("/login", response_model=TokenOut)
async def login(input: RegisterIn):
    user = fake_users_db.get(input.email)
    if not user or not verify_password(input.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    token = create_access_token({"sub": input.email})
    return {"access_token": token}