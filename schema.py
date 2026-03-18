from pydantic import BaseModel, Field
from typing import Optional

class DoctorCreate(BaseModel):
    name: str = Field(..., min_length=2)
    specialization: str
    fee: int
    experience_years: int
    is_available: bool = True

class AppointmentCreate(BaseModel):
    patient_name: str = Field(..., min_length=2)
    doctor_id: int
    date: str
    reason: str = Field(..., min_length=5)
    appointment_type: str = "in-person"
    senior_citizen: bool = False
