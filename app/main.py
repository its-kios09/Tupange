# main.py
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db_engine, check_db_connection, get_engine
from app.utils.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    custom_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = FastAPI(
    title="Tupange HealthCare Appointment Scheduling API",
    description="API for managing healthcare appointments, patients, doctors and medical records",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, custom_exception_handler)

@app.on_event("startup")
async def startup_event():
    logging.info("Starting up the Tupange HealthCare Appointment Scheduling API...")
    
    # Initialize database engine first
    await init_db_engine()
    
    # Check database connection
    if not await check_db_connection():
        raise RuntimeError("Failed to connect to database on startup")
    
    # Initialize database with tables and superuser
    try:
        from app.init_db import init_db
        await init_db()
        logging.info("Database initialization completed successfully")
    except Exception as e:
        logging.error(f"Database initialization failed: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    engine = get_engine()
    await engine.dispose()
    logging.info("Shutting down the Tupange HealthCare Appointment Scheduling API...")

@app.get("/health")
async def health_check():
    """Endpoint to check database and application health"""
    db_healthy = await check_db_connection()
    if not db_healthy:
        raise HTTPException(status_code=503, detail="Database unavailable")
    
    return {
        "status": "healthy",
        "database": "connected",
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Tupange HealthCare Appointment Scheduling API",
        "version": "1.0.0",
        "description": "API for managing healthcare appointments, patients, doctors and medical records",
        "documentation": {
            "openapi": "/api/v1/openapi.json",
            "redoc": "/redoc",
            "swagger": "/docs",
        },
        "health_check": "/health"
    }