from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.schemas.patient import Patient, PatientCreate, PatientUpdate, PatientProfileUpdate
from app.services.patient import PatientService
from app.services.auth import get_current_active_user, get_current_active_patient
from app.database import get_db
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=Patient)
async def create_patient(
    patient_in: PatientCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return await PatientService.create_patient(db, patient_in)

@router.get("/", response_model=List[Patient])
async def read_patients(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return await PatientService.get_patients(db, skip=skip, limit=limit)

@router.get("/me", response_model=Patient)
async def read_patient_profile(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_patient)
):
    return await PatientService.get_patient_by_user_id(db, current_user.id)

@router.put("/me", response_model=Patient)
async def update_patient_profile(
    patient_in: PatientProfileUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_patient)
):
    return await PatientService.update_patient_profile(db, current_user.id, patient_in)

@router.get("/{patient_id}", response_model=Patient)
async def read_patient(
    patient_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return await PatientService.get_patient(db, patient_id)

@router.put("/{patient_id}", response_model=Patient)
async def update_patient(
    patient_id: int,
    patient_in: PatientUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return await PatientService.update_patient(db, patient_id, patient_in)

@router.delete("/{patient_id}")
async def delete_patient(
    patient_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    await PatientService.delete_patient(db, patient_id)
    return {"message": "Patient deleted successfully"}