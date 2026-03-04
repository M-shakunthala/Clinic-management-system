# 🏥 Clinic Management System API

A comprehensive, production-ready FastAPI application for managing clinic operations including patients, doctors, appointments, and medical records.

## 🚀 Features

### 🔐 **Security & Authentication**
- **JWT Authentication** with OAuth2
- **Password Hashing** using bcrypt
- **Role-Based Access Control** (Admin, Doctor, Patient)
- **Protected Routes** with proper authorization

### 🏥 **Core Functionality**
- **Patient Management** - Registration and profile management
- **Doctor Management** - Doctor profiles and specializations
- **Appointment Scheduling** - With conflict detection and business logic
- **Medical Records** - Doctor-only medical record creation
- **User Management** - Multi-role user system

### 🔧 **Production Features**
- **Pagination & Filtering** - Efficient data retrieval
- **Global Exception Handling** - Robust error management
- **Comprehensive Logging** - Application monitoring
- **Input Validation** - Using Pydantic schemas
- **API Documentation** - Auto-generated Swagger UI

### 🐳 **DevOps Ready**
- **Docker Support** - Containerized deployment
- **Docker Compose** - Complete stack with PostgreSQL
- **Environment Configuration** - Secure credential management

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL
- **Authentication**: JWT + OAuth2
- **Security**: Passlib (bcrypt)
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Containerization**: Docker

## 🏃‍♂️ Quick Start

### Option 1: Local Development
```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Edit .env with your PostgreSQL credentials

# Run the application
uvicorn app.main:app --reload
```

### Option 2: Docker Deployment
```bash
# Start with Docker Compose
docker-compose up --build

# API will be available at http://localhost:8000
```

## 📚 API Documentation

Once running, access the interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔑 API Endpoints

### Authentication
- `POST /login` - User authentication
- `GET /me` - Get current user info

### Users
- `POST /users` - Create user
- `GET /users` - List users (Admin only)

### Doctors
- `POST /doctors` - Create doctor (Admin only)
- `GET /doctors` - List doctors
- `GET /doctors/{id}` - Get doctor details

### Patients
- `POST /patients` - Create patient
- `GET /patients` - List patients (Admin only)
- `GET /patients/{id}` - Get patient details

### Appointments
- `POST /appointments` - Create appointment (with conflict detection)
- `GET /appointments` - List appointments (role-filtered, paginated)
- `GET /appointments/{id}` - Get appointment details
- `GET /my-appointments` - Patient's own appointments

### Medical Records
- `POST /medical-records` - Create record (Doctor only)
- `GET /medical-records` - List records (role-filtered, paginated)
- `GET /medical-records/{id}` - Get record details

## 🔐 Role-Based Access Control

### Admin Users
- ✅ Create doctors
- ✅ View all users and patients
- ✅ Access all appointments and medical records

### Doctor Users
- ✅ View doctor listings
- ✅ Create medical records
- ✅ View their own appointments and records

### Patient Users
- ✅ Create appointments
- ✅ View their own appointments and medical records
- ❌ Cannot access other patients' data

## 🏗️ Project Structure

```
clinic-management-project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── database.py          # Database configuration
│   ├── auth.py              # Authentication & authorization
│   ├── routes.py            # API routes
│   └── utils.py             # Utility functions
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Complete stack setup
├── .env                    # Environment variables
└── README.md              # This file
```

## 🧪 Key Business Logic Features

### 🚫 **Appointment Conflict Detection**
```python
# Prevents double-booking doctors
existing_appointment = db.query(models.Appointment).filter(
    models.Appointment.doctor_id == appointment.doctor_id,
    models.Appointment.appointment_time == appointment.appointment_time,
    models.Appointment.status != "cancelled"
).first()

if existing_appointment:
    raise HTTPException(400, "Time slot already booked")
```

### 📄 **Pagination Support**
```python
# All listing endpoints support pagination
@router.get("/appointments")
def get_appointments(skip: int = 0, limit: int = 10):
    return db.query(models.Appointment).offset(skip).limit(limit).all()
```

## 🚀 Deployment Ready

Perfect for deployment on:
- **Render** - Easy deployment with free tier
- **Railway** - Git-based deployment  
- **Fly.io** - Global deployment
- **Docker** - Containerized deployment

## 🎯 Interview-Ready Features

✅ **Security Knowledge**: JWT + Password Hashing  
✅ **Authorization**: Role-based access control  
✅ **Business Logic**: Appointment conflict prevention  
✅ **Production Standards**: Error handling + logging  
✅ **Advanced FastAPI**: Dependency injection  
✅ **Docker**: Containerization & DevOps  

---

**🏆 A comprehensive, production-ready API perfect for showcasing backend development skills!**
