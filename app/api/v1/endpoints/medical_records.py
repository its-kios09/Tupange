from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.schemas.medical_record import (
    MedicalRecord, 
    MedicalRecordCreate, 
    MedicalRecordUpdate
)
from app.services.medical_record import MedicalRecordService
from app.services.auth import (
    get_current_active_user,
    get_current_active_patient,
    get_current_active_doctor
)
from app.database import get_db
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=MedicalRecord)
async def create_medical_record(
    record_in: MedicalRecordCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_doctor)
):
    return await MedicalRecordService.create_medical_record(db, record_in, current_user.id)

@router.get("/my-records", response_model=List[MedicalRecord])
async def read_my_medical_records(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_patient)
):
    return await MedicalRecordService.get_patient_records(db, current_user.id)

@router.get("/patient/{patient_id}", response_model=List[MedicalRecord])
async def read_patient_records(
    patient_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_doctor)
):
    return await MedicalRecordService.get_patient_records(db, patient_id)

@router.get("/{record_id}", response_model=MedicalRecord)
async def read_medical_record(
    record_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return await MedicalRecordService.get_medical_record(db, record_id)

@router.put("/{record_id}", response_model=MedicalRecord)
async def update_medical_record(
    record_id: int,
    record_in: MedicalRecordUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_doctor)
):
    return await MedicalRecordService.update_medical_record(db, record_id, record_in)

@router.delete("/{record_id}")
async def delete_medical_record(
    record_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_doctor)
):
    await MedicalRecordService.delete_medical_record(db, record_id)
    return {"message": "Medical record deleted successfully"}