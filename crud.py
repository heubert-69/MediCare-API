from sqlalchemy.orm import Session
from models import *

def get_doctors(db: Session):
    return db.query(models.Doctor).all()

def create_doctor(db: Session, doc):
    db_doc = models.Doctor(**doc.dict())
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc

def find_doctor(db, doctor_id):
    return db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()

def create_appointment(db, data, doctor, original_fee, final_fee):
    appt = models.Appointment(
        patient=data.patient_name,
        doctor_id=doctor.id,
        doctor=doctor.name,
        date=data.date,
        type=data.appointment_type,
        original_fee=original_fee,
        final_fee=final_fee,
        status="scheduled"
    )
    db.add(appt)
    db.commit()
    db.refresh(appt)
    return appt
