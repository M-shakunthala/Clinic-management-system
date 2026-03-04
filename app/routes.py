from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import timedelta
from . import models, schemas, auth
from .database import get_db
from .utils import hash_password, verify_password

router = APIRouter()

# Authentication Routes
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Doctor Routes (Admin only can create)
@router.post("/doctors", response_model=schemas.DoctorResponse)
def create_doctor(
    doctor: schemas.DoctorCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_admin)
):
    new_doctor = models.Doctor(**doctor.dict())
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)
    return new_doctor

@router.get("/doctors", response_model=List[schemas.DoctorResponse])
def get_doctors(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    doctors = db.query(models.Doctor).all()
    return doctors

@router.get("/doctors/{doctor_id}", response_model=schemas.DoctorResponse)
def get_doctor(
    doctor_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

# Patient Routes
@router.post("/patients", response_model=schemas.PatientResponse)
def create_patient(
    patient: schemas.PatientCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    new_patient = models.Patient(**patient.dict())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient

@router.get("/patients", response_model=List[schemas.PatientResponse])
def get_patients(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_admin)  # Only admin can see all patients
):
    patients = db.query(models.Patient).all()
    return patients

@router.get("/patients/{patient_id}", response_model=schemas.PatientResponse)
def get_patient(
    patient_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

# User Routes
@router.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Hash the password before storing
    hashed_password = hash_password(user.password)
    user_data = user.dict()
    user_data["password"] = hashed_password
    new_user = models.User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/users", response_model=List[schemas.UserResponse])
def get_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_admin)  # Only admin can see all users
):
    users = db.query(models.User).all()
    return users

@router.get("/me", response_model=schemas.UserResponse)
def get_current_user_info(current_user: models.User = Depends(auth.get_current_active_user)):
    return current_user

# Appointment Routes with Business Logic
@router.post("/appointments", response_model=schemas.AppointmentResponse)
def create_appointment(
    appointment: schemas.AppointmentCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    # Verify doctor and patient exist
    doctor = db.query(models.Doctor).filter(models.Doctor.id == appointment.doctor_id).first()
    patient = db.query(models.Patient).filter(models.Patient.id == appointment.patient_id).first()
    
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # STEP 15: Check for appointment conflicts (IMPORTANT BUSINESS LOGIC)
    existing_appointment = db.query(models.Appointment).filter(
        models.Appointment.doctor_id == appointment.doctor_id,
        models.Appointment.appointment_time == appointment.appointment_time,
        models.Appointment.status != "cancelled"  # Don't count cancelled appointments
    ).first()
    
    if existing_appointment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Time slot already booked. Doctor {doctor.name} has an appointment at {appointment.appointment_time}"
        )
    
    new_appointment = models.Appointment(**appointment.dict())
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment

# STEP 17: Add Pagination & Filtering
@router.get("/appointments", response_model=List[schemas.AppointmentResponse])
def get_appointments(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    # Role-based filtering with pagination
    if current_user.role == "admin":
        # Admin can see all appointments
        appointments = db.query(models.Appointment).offset(skip).limit(limit).all()
    elif current_user.role == "doctor":
        # Doctor can see their own appointments
        appointments = db.query(models.Appointment).join(models.Doctor).filter(
            models.Doctor.name == current_user.email  # Assuming doctor email matches their name
        ).offset(skip).limit(limit).all()
    else:  # patient
        # Patient can see their own appointments
        appointments = db.query(models.Appointment).join(models.Patient).filter(
            models.Patient.name == current_user.email  # Assuming patient email matches their name
        ).offset(skip).limit(limit).all()
    
    return appointments

@router.get("/appointments/{appointment_id}", response_model=schemas.AppointmentResponse)
def get_appointment(
    appointment_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    # Role-based access control
    if current_user.role == "patient":
        # Patients can only see their own appointments
        patient = db.query(models.Patient).filter(models.Patient.name == current_user.email).first()
        if not patient or appointment.patient_id != patient.id:
            raise HTTPException(status_code=403, detail="Access denied")
    
    return appointment

# My appointments endpoint for patients
@router.get("/my-appointments", response_model=List[schemas.AppointmentResponse])
def get_my_appointments(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_patient)
):
    # Find patient record by email
    patient = db.query(models.Patient).filter(models.Patient.name == current_user.email).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient record not found")
    
    appointments = db.query(models.Appointment).filter(
        models.Appointment.patient_id == patient.id
    ).offset(skip).limit(limit).all()
    return appointments


# STEP 16: Medical Records Routes (Doctor-only)
@router.post("/medical-records", response_model=schemas.MedicalRecordResponse)
def create_medical_record(
    record: schemas.MedicalRecordCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_doctor)
):
    # Verify patient exists
    patient = db.query(models.Patient).filter(models.Patient.id == record.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Find doctor record by email (assuming email matches name)
    doctor = db.query(models.Doctor).filter(models.Doctor.name == current_user.email).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor record not found")
    
    record_data = record.dict()
    record_data["doctor_id"] = doctor.id
    new_record = models.MedicalRecord(**record_data)
    
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

@router.get("/medical-records", response_model=List[schemas.MedicalRecordResponse])
def get_medical_records(
    skip: int = 0,
    limit: int = 10,
    patient_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    query = db.query(models.MedicalRecord)
    
    # Role-based filtering
    if current_user.role == "doctor":
        # Doctor can see records they created
        doctor = db.query(models.Doctor).filter(models.Doctor.name == current_user.email).first()
        if doctor:
            query = query.filter(models.MedicalRecord.doctor_id == doctor.id)
    elif current_user.role == "patient":
        # Patient can see their own records
        patient = db.query(models.Patient).filter(models.Patient.name == current_user.email).first()
        if patient:
            query = query.filter(models.MedicalRecord.patient_id == patient.id)
    # Admin can see all records (no additional filtering)
    
    # Optional patient filter
    if patient_id:
        query = query.filter(models.MedicalRecord.patient_id == patient_id)
    
    return query.offset(skip).limit(limit).all()

@router.get("/medical-records/{record_id}", response_model=schemas.MedicalRecordResponse)
def get_medical_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    record = db.query(models.MedicalRecord).filter(models.MedicalRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Medical record not found")
    
    # Role-based access control
    if current_user.role == "patient":
        patient = db.query(models.Patient).filter(models.Patient.name == current_user.email).first()
        if not patient or record.patient_id != patient.id:
            raise HTTPException(status_code=403, detail="Access denied")
    elif current_user.role == "doctor":
        doctor = db.query(models.Doctor).filter(models.Doctor.name == current_user.email).first()
        if not doctor or record.doctor_id != doctor.id:
            raise HTTPException(status_code=403, detail="Access denied")
    
    return record
