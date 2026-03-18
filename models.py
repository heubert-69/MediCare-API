from sqlalchemy import Column, Integer, String, Boolean, Float
from database import Base

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    specialization = Column(String)
    fee = Column(Integer)
    experience_years = Column(Integer)
    is_available = Column(Boolean, default=True)

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient = Column(String)
    doctor_id = Column(Integer)
    doctor = Column(String)
    date = Column(String)
    type = Column(String)
    original_fee = Column(Float)
    final_fee = Column(Float)
    status = Column(String, default="scheduled")
