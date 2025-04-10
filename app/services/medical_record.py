from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.models.medical_record import MedicalRecord
from app.schemas.medical_record import MedicalRecordCreate, MedicalRecordUpdate
from app.utils.exceptions import MedicalRecordNotFoundException

class MedicalRecordService:
    @staticmethod
    async def create_medical_record(
        db: AsyncSession, 
        record_in: MedicalRecordCreate
    ) -> MedicalRecord:
        record = MedicalRecord(**record_in.dict())
        db.add(record)
        await db.commit()
        await db.refresh(record)
        return record

    @staticmethod
    async def get_medical_record(db: AsyncSession, record_id: int) -> MedicalRecord:
        record = await db.get(MedicalRecord, record_id)
        if not record:
            raise MedicalRecordNotFoundException(record_id)
        return record

    @staticmethod
    async def get_patient_records(
        db: AsyncSession, 
        patient_id: int
    ) -> List[MedicalRecord]:
        result = await db.execute(
            select(MedicalRecord)
            .where(MedicalRecord.patient_id == patient_id)
            .order_by(MedicalRecord.id)
        )
        return result.scalars().all()

    @staticmethod
    async def update_medical_record(
        db: AsyncSession, 
        record_id: int, 
        record_in: MedicalRecordUpdate
    ) -> MedicalRecord:
        record = await MedicalRecordService.get_medical_record(db, record_id)
        update_data = record_in.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(record, field, value)
            
        await db.commit()
        await db.refresh(record)
        return record

    @staticmethod
    async def delete_medical_record(db: AsyncSession, record_id: int) -> None:
        record = await MedicalRecordService.get_medical_record(db, record_id)
        await db.delete(record)
        await db.commit()