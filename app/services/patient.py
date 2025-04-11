from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy import select

from app.models.user import User 
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate
from app.utils.exceptions import PatientNotFoundException
from app.utils.redis_client import redis_client  # Import the Redis client

class PatientService:
    @staticmethod
    async def create_patient(db: AsyncSession, patient_in: PatientCreate):
        # Verify user exists first
        user = await db.get(User, patient_in.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with id {patient_in.user_id} does not exist"
            )
        
        # Create the patient
        patient = Patient(
            user_id=patient_in.user_id,
            first_name=patient_in.first_name,
            last_name=patient_in.last_name,
            date_of_birth=patient_in.date_of_birth,
            gender=patient_in.gender,
            phone_number=patient_in.phone_number,
            address=patient_in.address,
            insurance_provider=patient_in.insurance_provider,
            insurance_number=patient_in.insurance_number
        )
        
        db.add(patient)
        await db.commit()
        await db.refresh(patient)
        
        # Log the operation in Redis
        await redis_client.log_operation(
            operation="create_patient",
            key=f"patient:{patient.id}",
            value=f"{patient.first_name} {patient.last_name}"
        )
        
        return patient

    @staticmethod
    async def get_patient(db: AsyncSession, patient_id: int) -> Patient:
        patient = await db.get(Patient, patient_id)
        if not patient:
            raise PatientNotFoundException(patient_id)
        
        # Log the operation in Redis
        await redis_client.log_operation(
            operation="get_patient",
            key=f"patient:{patient_id}"
        )
        
        return patient

    @staticmethod
    async def get_patients(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Patient]:
       result = await db.execute(select(Patient).offset(skip).limit(limit))
       
       # Log the operation in Redis
       await redis_client.log_operation(
           operation="get_patients",
           value=f"skip:{skip}, limit:{limit}"
       )
       
       return result.scalars().all()

    @staticmethod
    async def update_patient(
        db: AsyncSession, 
        patient_id: int, 
        patient_in: PatientUpdate
    ) -> Patient:
        patient = await PatientService.get_patient(db, patient_id)
        update_data = patient_in.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(patient, field, value)
            
        await db.commit()
        await db.refresh(patient)
        
        # Log the operation in Redis
        await redis_client.log_operation(
            operation="update_patient",
            key=f"patient:{patient_id}",
            value=str(update_data)
        )
        
        return patient

    @staticmethod
    async def delete_patient(db: AsyncSession, patient_id: int) -> None:
        patient = await PatientService.get_patient(db, patient_id)
        await db.delete(patient)
        await db.commit()
        
        # Log the operation in Redis
        await redis_client.log_operation(
            operation="delete_patient",
            key=f"patient:{patient_id}",
            value=f"{patient.first_name} {patient.last_name}"
        )