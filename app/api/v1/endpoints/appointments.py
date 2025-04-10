from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.schemas.appointment import (
    Appointment, 
    AppointmentCreate, 
    AppointmentUpdate,
    AppointmentStatusUpdate,
    AppointmentSlot
)
from app.services.appointment import AppointmentService
from app.services.auth import (
    get_current_active_user,
    get_current_active_patient,
    get_current_active_doctor
)
from app.database import get_db
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=Appointment)
async def create_appointment(
    appointment_in: AppointmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_patient)
):
    return await AppointmentService.create_appointment(db, appointment_in, current_user.id)

@router.get("/", response_model=List[Appointment])
async def read_appointments(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return await AppointmentService.get_appointments(db, skip=skip, limit=limit)

@router.get("/my-appointments", response_model=List[Appointment])
async def read_my_appointments(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_patient)
):
    return await AppointmentService.get_patient_appointments(db, current_user.id)

@router.get("/doctor-appointments", response_model=List[Appointment])
async def read_doctor_appointments(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_doctor)
):
    return await AppointmentService.get_doctor_appointments(db, current_user.id)

@router.get("/available-slots/{doctor_id}", response_model=List[AppointmentSlot])
async def get_available_slots(
    doctor_id: int,
    date: str,  # YYYY-MM-DD format
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return await AppointmentService.get_available_slots(db, doctor_id, date)

@router.put("/{appointment_id}/status", response_model=Appointment)
async def update_appointment_status(
    appointment_id: int,
    status_update: AppointmentStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_doctor)
):
    return await AppointmentService.update_appointment_status(
        db, appointment_id, status_update.status
    )

@router.put("/{appointment_id}", response_model=Appointment)
async def update_appointment(
    appointment_id: int,
    appointment_in: AppointmentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return await AppointmentService.update_appointment(db, appointment_id, appointment_in)

@router.post("/{appointment_id}/cancel", response_model=Appointment)
async def cancel_appointment(
    appointment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return await AppointmentService.cancel_appointment(db, appointment_id)

@router.delete("/{appointment_id}")
async def delete_appointment(
    appointment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    await AppointmentService.delete_appointment(db, appointment_id)
    return {"message": "Appointment deleted successfully"}