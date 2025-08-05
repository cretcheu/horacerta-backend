# hora_certa_app/routes/appointments.py
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from hora_certa_app.db import SessionLocal
from hora_certa_app.models.appointment import Appointment
from hora_certa_app.schemas import (
    AppointmentCreate,
    AppointmentRead,
    AppointmentUpdate,
)
from hora_certa_app.routes.auth import get_current_user
from hora_certa_app.schemas import UserRead  # caso queira tipar

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/",
    response_model=AppointmentRead,
    status_code=status.HTTP_201_CREATED
)
def create_appointment(
    appt_in: AppointmentCreate,
    current_user: UserRead = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    appt = Appointment(
        user_id=current_user.id,
        start=appt_in.start,
        end=appt_in.end,
        notes=appt_in.notes or ""
    )
    db.add(appt)
    db.commit()
    db.refresh(appt)
    return appt

@router.get("/", response_model=list[AppointmentRead])
def list_appointments(
    current_user: UserRead = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Appointment).filter_by(user_id=current_user.id).all()

@router.put("/{appt_id}", response_model=AppointmentRead)
def update_appointment(
    appt_id: int,
    appt_in: AppointmentUpdate,
    current_user: UserRead = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    appt = db.get(Appointment, appt_id)
    if not appt or appt.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    for field, val in appt_in.dict(exclude_unset=True).items():
        setattr(appt, field, val)
    db.commit()
    db.refresh(appt)
    return appt

@router.delete("/{appt_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment(
    appt_id: int,
    current_user: UserRead = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    appt = db.get(Appointment, appt_id)
    if not appt or appt.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    db.delete(appt)
    db.commit()
    return