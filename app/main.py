import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db_engine, check_db_connection, get_engine
from app.api.v1.api_v1 import api_router
from app.utils.redis_client import redis_client 
from app.utils.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    custom_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

# Initialize logger
logger = logging.getLogger(__name__)
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

app.include_router(api_router, prefix="/api/v1", tags=["v1"])

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, custom_exception_handler)

@app.on_event("startup")
async def startup_event():
    logger.info("✅ Starting up the Tupange HealthCare Appointment Scheduling API...")
    
    try:
        # Initialize database engine and session maker
        engine = await init_db_engine()
    
        # Verify database connection
        if not await check_db_connection():
            raise RuntimeError("Failed to connect to database on startup")
        
        # Initialize database schema and superuser
        from app.init_db import init_db
        await init_db()
        logger.info("✅ Database initialization completed successfully")

        # Initialize Redis client
        await redis_client.connect()
        
        # Verify Redis connection
        if not await redis_client.is_healthy():
            logger.error("Redis connection failed on startup")
        else:
            logger.info("✅ Redis connection verified successfully")

    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    try:
        engine = get_engine()
        await engine.dispose()
        await redis_client.disconnect()
        logger.info("Shutting down the Tupange HealthCare Appointment Scheduling API...")
    except Exception as e:
        logger.error(f"Shutdown error: {e}")

@app.get("/health")
async def health_check():
    """Endpoint to check database and application health"""
    try:
        db_healthy = await check_db_connection()
        redis_healthy = await redis_client.is_healthy()
        
        if not db_healthy or not redis_healthy:
            status_detail = {
                "database": "unavailable" if not db_healthy else "connected",
                "redis": "unavailable" if not redis_healthy else "connected"
            }
            raise HTTPException(
                status_code=503,
                detail=status_detail
            )
        
        return {
            "status": "healthy",
            "database": "connected",
            "redis": "connected",
            "version": "1.0.0"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=500,
            detail="Health check failed"
        )

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