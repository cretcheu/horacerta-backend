# hora_certa_app/schemas.py

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


# --- Usuário ---

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserRead(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True


# --- Token ---

class Token(BaseModel):
    access_token: str
    token_type: str


# --- Agendamentos ---

class AppointmentBase(BaseModel):
    start: datetime
    end:   datetime
    notes: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    ...

class AppointmentRead(AppointmentBase):
    id:      int
    user_id: int

    class Config:
        orm_mode = True

class AppointmentUpdate(AppointmentBase):
    ...