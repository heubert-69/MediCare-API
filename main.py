from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import *
from schema import *
from crud import *

Base.metadata.create_all(bind=engine)


app = FastAPI()

doctors = [
    {"id": 1, "name": "Dr. Smith", "specialization": "Cardiologist", "fee": 800, "experience_years": 15, "is_available": True},
    {"id": 2, "name": "Dr. Lee", "specialization": "Dermatologist", "fee": 500, "experience_years": 8, "is_available": True},
    {"id": 3, "name": "Dr. Patel", "specialization": "Pediatrician", "fee": 400, "experience_years": 10, "is_available": False},
    {"id": 4, "name": "Dr. Cruz", "specialization": "General", "fee": 300, "experience_years": 5, "is_available": True},
    {"id": 5, "name": "Dr. Kim", "specialization": "Cardiologist", "fee": 900, "experience_years": 20, "is_available": True},
    {"id": 6, "name": "Dr. Tan", "specialization": "Dermatologist", "fee": 450, "experience_years": 7, "is_available": False}
]

appointments = []
appt_counter = 1

class AppointmentRequest(BaseModel):
    patient_name: str = Field(..., min_length=2)
    doctor_id: int = Field(..., gt=0)
    date: str = Field(..., min_length=8)
    reason: str = Field(..., min_length=5)
    appointment_type: str = "in-person"
    senior_citizen: bool = False

class NewDoctor(BaseModel):
    name: str = Field(..., min_length=2)
    specialization: str = Field(..., min_length=2)
    fee: int = Field(..., gt=0)
    experience_years: int = Field(..., gt=0)
    is_available: bool = True

def find_doctor(doctor_id):
    for d in doctors:
        if d["id"] == doctor_id:
            return d
    return None

def calculate_fee(base_fee, appointment_type, senior=False):
    if appointment_type == "video":
        fee = base_fee * 0.8
    elif appointment_type == "emergency":
        fee = base_fee * 1.5
    else:
        fee = base_fee
    final_fee = fee * 0.85 if senior else fee
    return fee, final_fee

def filter_doctors_logic(specialization, max_fee, min_experience, is_available):
    result = doctors
    if specialization is not None:
        result = [d for d in result if d["specialization"].lower() == specialization.lower()]
    if max_fee is not None:
        result = [d for d in result if d["fee"] <= max_fee]
    if min_experience is not None:
        result = [d for d in result if d["experience_years"] >= min_experience]
    if is_available is not None:
        result = [d for d in result if d["is_available"] == is_available]
    return result

@app.get("/")
def root():
    return {"message": "Welcome to MediCare Clinic"}

@app.get("/doctors")
def get_doctors():
    available = [d for d in doctors if d["is_available"]]
    return {"total": len(doctors), "available_count": len(available), "doctors": doctors}

@app.get("/doctors/summary")
def doctors_summary():
    available = [d for d in doctors if d["is_available"]]
    most_exp = max(doctors, key=lambda x: x["experience_years"])
    cheapest = min(doctors, key=lambda x: x["fee"])
    spec_count = {}
    for d in doctors:
        spec_count[d["specialization"]] = spec_count.get(d["specialization"], 0) + 1
    return {
        "total": len(doctors),
        "available": len(available),
        "most_experienced": most_exp["name"],
        "cheapest_fee": cheapest["fee"],
        "specializations": spec_count
    }

@app.get("/doctors/filter")
def filter_doctors(specialization: Optional[str] = None, max_fee: Optional[int] = None, min_experience: Optional[int] = None, is_available: Optional[bool] = None):
    return {"results": filter_doctors_logic(specialization, max_fee, min_experience, is_available)}

@app.get("/doctors/search")
def search_doctors(keyword: str):
    result = [d for d in doctors if keyword.lower() in d["name"].lower() or keyword.lower() in d["specialization"].lower()]
    if not result:
        return {"message": f"No doctors found for: {keyword}"}
    return {"total_found": len(result), "doctors": result}

@app.get("/doctors/sort")
def sort_doctors(sort_by: str = "fee", order: str = "asc"):
    if sort_by not in ["fee", "name", "experience_years"]:
        return {"error": "invalid sort_by"}
    reverse = True if order == "desc" else False
    return {"sort_by": sort_by, "order": order, "doctors": sorted(doctors, key=lambda x: x[sort_by], reverse=reverse)}

@app.get("/doctors/page")
def paginate_doctors(page: int = 1, limit: int = 3):
    total = len(doctors)
    total_pages = (total + limit - 1) // limit
    start = (page - 1) * limit
    end = start + limit
    return {"page": page, "limit": limit, "total_pages": total_pages, "doctors": doctors[start:end]}

@app.get("/doctors/browse")
def browse_doctors(keyword: Optional[str] = None, sort_by: str = "fee", order: str = "asc", page: int = 1, limit: int = 4):
    result = doctors
    if keyword:
        result = [d for d in result if keyword.lower() in d["name"].lower() or keyword.lower() in d["specialization"].lower()]
    if sort_by not in ["fee", "name", "experience_years"]:
        return {"error": "invalid sort_by"}
    reverse = True if order == "desc" else False
    result = sorted(result, key=lambda x: x[sort_by], reverse=reverse)
    total = len(result)
    total_pages = (total + limit - 1) // limit
    start = (page - 1) * limit
    end = start + limit
    return {"total": total, "total_pages": total_pages, "doctors": result[start:end]}

@app.post("/doctors")
def add_doctor(new_doc: NewDoctor):
    for d in doctors:
        if d["name"].lower() == new_doc.name.lower():
            raise HTTPException(status_code=400, detail="Doctor already exists")
    new_id = len(doctors) + 1
    doc = new_doc.dict()
    doc["id"] = new_id
    doctors.append(doc)
    return doc

@app.put("/doctors/{doctor_id}")
def update_doctor(doctor_id: int, fee: Optional[int] = None, is_available: Optional[bool] = None):
    doc = find_doctor(doctor_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Doctor not found")
    if fee is not None:
        doc["fee"] = fee
    if is_available is not None:
        doc["is_available"] = is_available
    return doc

@app.delete("/doctors/{doctor_id}")
def delete_doctor(doctor_id: int):
    doc = find_doctor(doctor_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Doctor not found")
    for a in appointments:
        if a["doctor_id"] == doctor_id and a["status"] == "scheduled":
            return {"error": "Doctor has active appointments"}
    doctors.remove(doc)
    return {"message": "Doctor deleted"}

@app.get("/doctors/{doctor_id}")
def get_doctor(doctor_id: int):
    doc = find_doctor(doctor_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doc

@app.get("/appointments")
def get_appointments():
    return {"total": len(appointments), "appointments": appointments}

@app.get("/appointments/active")
def active_appointments():
    return {"appointments": [a for a in appointments if a["status"] in ["scheduled", "confirmed"]]}

@app.get("/appointments/by-doctor/{doctor_id}")
def appointments_by_doctor(doctor_id: int):
    return {"appointments": [a for a in appointments if a["doctor_id"] == doctor_id]}

@app.get("/appointments/search")
def search_appointments(patient_name: str):
    result = [a for a in appointments if patient_name.lower() in a["patient"].lower()]
    if not result:
        return {"message": f"No appointments for: {patient_name}"}
    return {"total": len(result), "appointments": result}

@app.get("/appointments/sort")
def sort_appointments(sort_by: str = "fee", order: str = "asc"):
    reverse = True if order == "desc" else False
    return {"appointments": sorted(appointments, key=lambda x: x[sort_by], reverse=reverse)}

@app.get("/appointments/page")
def paginate_appointments(page: int = 1, limit: int = 3):
    total = len(appointments)
    total_pages = (total + limit - 1) // limit
    start = (page - 1) * limit
    end = start + limit
    return {"page": page, "limit": limit, "total_pages": total_pages, "appointments": appointments[start:end]}

@app.post("/appointments")
def create_appointment(req: AppointmentRequest):
    global appt_counter
    doc = find_doctor(req.doctor_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Doctor not found")
    if not doc["is_available"]:
        return {"error": "Doctor not available"}
    base_fee, final_fee = calculate_fee(doc["fee"], req.appointment_type, req.senior_citizen)
    appointment = {
        "appointment_id": appt_counter,
        "patient": req.patient_name,
        "doctor_id": doc["id"],
        "doctor": doc["name"],
        "date": req.date,
        "type": req.appointment_type,
        "original_fee": base_fee,
        "final_fee": final_fee,
        "status": "scheduled"
    }
    appointments.append(appointment)
    appt_counter += 1
    doc["is_available"] = False
    return appointment

@app.post("/appointments/{appointment_id}/confirm")
def confirm_appointment(appointment_id: int):
    for a in appointments:
        if a["appointment_id"] == appointment_id:
            a["status"] = "confirmed"
            return a
    raise HTTPException(status_code=404, detail="Appointment not found")

@app.post("/appointments/{appointment_id}/cancel")
def cancel_appointment(appointment_id: int):
    for a in appointments:
        if a["appointment_id"] == appointment_id:
            a["status"] = "cancelled"
            doc = find_doctor(a["doctor_id"])
            if doc:
                doc["is_available"] = True
            return a
    raise HTTPException(status_code=404, detail="Appointment not found")

@app.post("/appointments/{appointment_id}/complete")
def complete_appointment(appointment_id: int):
    for a in appointments:
        if a["appointment_id"] == appointment_id:
            a["status"] = "completed"
            return a
    raise HTTPException(status_code=404, detail="Appointment not found")
