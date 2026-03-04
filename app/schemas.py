from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# User Schemas
class UserCreate(BaseModel):
    email: str
    password: str
    role: str

class UserResponse(BaseModel):
    id: int
    email: str
    role: str
    
    class Config:
        from_attributes = True


# Doctor Schemas
class DoctorCreate(BaseModel):
    name: str
    specialization: str
    phone: str

class DoctorResponse(BaseModel):
    id: int
    name: str
    specialization: str
    phone: str
    
    class Config:
        from_attributes = True


# Patient Schemas
class PatientCreate(BaseModel):
    name: str
    age: int
    phone: str

class PatientResponse(BaseModel):
    id: int
    name: str
    age: int
    phone: str
    
    class Config:
        from_attributes = True


# Appointment Schemas
class AppointmentCreate(BaseModel):
    doctor_id: int
    patient_id: int
    appointment_time: datetime

class AppointmentResponse(BaseModel):
    id: int
    doctor_id: int
    patient_id: int
    appointment_time: datetime
    status: str
    notes: Optional[str] = None
    
    class Config:
        from_attributes = True


# Medical Record Schemas
class MedicalRecordCreate(BaseModel):
    patient_id: int
    diagnosis: str
    prescription: Optional[str] = None
    notes: Optional[str] = None

class MedicalRecordResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    diagnosis: str
    prescription: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
