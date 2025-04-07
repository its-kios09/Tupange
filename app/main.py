import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = FastAPI(
    title = "Tupange HealthCare Appointment Scheduling API",
    description = "API for managing healthcare appointments, patients, doctors and medical records",
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

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Tupange HealthCare Appointment Scheduling API",
        "version": "1.0.0",
        "description": "API for managing healthcare appointments, patients, doctors and medical records",
        "documentation": {
            "openapi": "/api/v1/openapi.json",
            "redoc": "/docs",
            "swagger": "/docs",
        },
    }