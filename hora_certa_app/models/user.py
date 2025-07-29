# hora_certa_app/models/user.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from hora_certa_app.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Relacionamento um-para-muitos com Appointment
    appointments = relationship(
        "Appointment",
        back_populates="user",
        cascade="all, delete-orphan"
    )