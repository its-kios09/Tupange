from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.schemas.patient import Patient 

from app.schemas.doctor import (
    Doctor, 
    DoctorCreate, 
    DoctorUpdate,
    DoctorProfileUpdate,
    DoctorAvailability,
    DoctorAvailabilityCreate,
    DoctorAvailabilityUpdate
)
from app.services.doctor import DoctorService
from app.services.auth import get_current_active_user, get_current_active_doctor
from app.database import get_db
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=Doctor)
async def create_doctor(
    doctor_in: DoctorCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return await DoctorService.create_doctor(db, doctor_in)

@router.get("/", response_model=List[Doctor])
async def read_doctors(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return await DoctorService.get_doctors(db, skip=skip, limit=limit)

@router.get("/me", response_model=Doctor)
async def read_doctor_profile(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_doctor)
):
    return await DoctorService.get_doctor_by_user_id(db, current_user.id)

@router.put("/me", response_model=Doctor)
async def update_doctor_profile(
    doctor_in: DoctorProfileUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_doctor)
):
    return await DoctorService.update_doctor_profile(db, current_user.id, doctor_in)

@router.get("/{doctor_id}", response_model=Doctor)
async def read_doctor(
    doctor_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return await DoctorService.get_doctor(db, doctor_id)

@router.put("/{doctor_id}", response_model=Doctor)
async def update_doctor(
    doctor_id: int,
    doctor_in: DoctorUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return await DoctorService.update_doctor(db, doctor_id, doctor_in)

@router.delete("/{doctor_id}")
async def delete_doctor(
    doctor_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    await DoctorService.delete_doctor(db, doctor_id)
    return {"message": "Doctor deleted successfully"}

@router.post("/availability", response_model=DoctorAvailability)
async def add_doctor_availability(
    availability_in: DoctorAvailabilityCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_doctor)
):
    return await DoctorService.add_availability(db, current_user.id, availability_in)

@router.get("/availability", response_model=List[DoctorAvailability])
async def get_doctor_availability(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_doctor)
):
    return await DoctorService.get_doctor_availability(db, current_user.id)

@router.put("/availability/{availability_id}", response_model=DoctorAvailability)
async def update_doctor_availability(
    availability_id: int,
    availability_in: DoctorAvailabilityUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_doctor)
):
    return await DoctorService.update_availability(db, availability_id, availability_in)

@router.delete("/availability/{availability_id}")
async def delete_doctor_availability(
    availability_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_doctor)
):
    await DoctorService.delete_availability(db, availability_id)
    return {"message": "Availability slot deleted successfully"}

@router.get("/my-patients", response_model=List[Patient])
async def get_my_patients(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_doctor)
):
    return await DoctorService.get_my_patients(db, current_user.id)