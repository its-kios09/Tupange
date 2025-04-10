from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from app.models.doctor import Doctor, DoctorAvailability
from app.schemas.doctor import (
    DoctorCreate, 
    DoctorUpdate, 
    DoctorAvailabilityCreate, 
    DoctorAvailability
)
from app.utils.exceptions import DoctorNotFoundException

class DoctorService:
    @staticmethod
    async def create_doctor(db: AsyncSession, doctor_in: DoctorCreate) -> Doctor:
        doctor = Doctor(**doctor_in.dict())
        db.add(doctor)
        await db.commit()
        await db.refresh(doctor)
        return doctor

    @staticmethod
    async def get_doctor(db: AsyncSession, doctor_id: int) -> Doctor:
        doctor = await db.get(Doctor, doctor_id)
        if not doctor:
            raise DoctorNotFoundException(doctor_id)
        return doctor

    @staticmethod
    async def get_doctors(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Doctor]:
        result = await db.execute(select(Doctor).offset(skip).limit(limit))
        return result.scalars().all()

    @staticmethod
    async def update_doctor(
        db: AsyncSession, 
        doctor_id: int, 
        doctor_in: DoctorUpdate
    ) -> Doctor:
        doctor = await DoctorService.get_doctor(db, doctor_id)
        update_data = doctor_in.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(doctor, field, value)
            
        await db.commit()
        await db.refresh(doctor)
        return doctor

    @staticmethod
    async def delete_doctor(db: AsyncSession, doctor_id: int) -> None:
        doctor = await DoctorService.get_doctor(db, doctor_id)
        await db.delete(doctor)
        await db.commit()

    @staticmethod
    async def add_availability(
        db: AsyncSession, 
        availability_in: DoctorAvailabilityCreate
    ) -> DoctorAvailability:
        availability = DoctorAvailability(**availability_in.dict())
        db.add(availability)
        await db.commit()
        await db.refresh(availability)
        return availability

    @staticmethod
    async def get_doctor_availability(
        db: AsyncSession, 
        doctor_id: int
    ) -> List[DoctorAvailability]:
        result = await db.execute(
            select(DoctorAvailability)
            .where(DoctorAvailability.doctor_id == doctor_id)
        )
        return result.scalars().all()