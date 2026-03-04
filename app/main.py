import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .routes import router
from .database import engine
from .models import Base

# STEP 19: Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Clinic Management System", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables automatically
Base.metadata.create_all(bind=engine)

# STEP 18: Global Exception Handling
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"}
    )

# Include the router with all CRUD routes
app.include_router(router)

@app.get("/")
def home():
    logger.info("Home endpoint accessed")
    return {"message": "Clinic Management System"}

@app.get("/test")
def test():
    logger.info("Test endpoint accessed")
    return {"status": "API is working!", "message": "Database connection will be added once credentials are correct"}
