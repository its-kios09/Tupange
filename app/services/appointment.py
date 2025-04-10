from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from fastapi import HTTPException, status
from app.models.appointment import Appointment, AppointmentStatus
from app.models.doctor import DoctorAvailability
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate
from app.utils.exceptions import (
    AppointmentNotFoundException,
    DoctorNotAvailableException,
    AppointmentConflictException
)

class AppointmentService:
    @staticmethod
    async def create_appointment(
        db: AsyncSession, 
        appointment_in: AppointmentCreate
    ) -> Appointment:
        # Check doctor availability
        if not await AppointmentService.is_doctor_available(
            db, 
            appointment_in.doctor_id, 
            appointment_in.scheduled_time, 
            appointment_in.end_time
        ):
            raise DoctorNotAvailableException(appointment_in.doctor_id)
            
        # Check for conflicting appointments
        if await AppointmentService.has_conflicting_appointment(
            db,
            appointment_in.doctor_id,
            appointment_in.scheduled_time,
            appointment_in.end_time
        ):
            raise AppointmentConflictException()
            
        appointment = Appointment(**appointment_in.dict())
        db.add(appointment)
        await db.commit()
        await db.refresh(appointment)
        return appointment

    @staticmethod
    async def get_appointment(db: AsyncSession, appointment_id: int) -> Appointment:
        appointment = await db.get(Appointment, appointment_id)
        if not appointment:
            raise AppointmentNotFoundException(appointment_id)
        return appointment

    @staticmethod
    async def get_appointments(
        db: AsyncSession, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Appointment]:
        result = await db.execute(select(Appointment).offset(skip).limit(limit))
        return result.scalars().all()

    @staticmethod
    async def get_patient_appointments(
        db: AsyncSession, 
        patient_id: int
    ) -> List[Appointment]:
        result = await db.execute(
            select(Appointment)
            .where(Appointment.patient_id == patient_id)
            .order_by(Appointment.scheduled_time)
        )
        return result.scalars().all()

    @staticmethod
    async def get_doctor_appointments(
        db: AsyncSession, 
        doctor_id: int
    ) -> List[Appointment]:
        result = await db.execute(
            select(Appointment)
            .where(Appointment.doctor_id == doctor_id)
            .order_by(Appointment.scheduled_time)
        )
        return result.scalars().all()

    @staticmethod
    async def update_appointment(
        db: AsyncSession, 
        appointment_id: int, 
        appointment_in: AppointmentUpdate
    ) -> Appointment:
        appointment = await AppointmentService.get_appointment(db, appointment_id)
        update_data = appointment_in.dict(exclude_unset=True)
        
        # If time is being updated, check availability
        if 'scheduled_time' in update_data or 'end_time' in update_data:
            scheduled_time = update_data.get('scheduled_time', appointment.scheduled_time)
            end_time = update_data.get('end_time', appointment.end_time)
            
            if not await AppointmentService.is_doctor_available(
                db, 
                appointment.doctor_id, 
                scheduled_time, 
                end_time,
                exclude_appointment_id=appointment_id
            ):
                raise DoctorNotAvailableException(appointment.doctor_id)
                
            if await AppointmentService.has_conflicting_appointment(
                db,
                appointment.doctor_id,
                scheduled_time,
                end_time,
                exclude_appointment_id=appointment_id
            ):
                raise AppointmentConflictException()
        
        for field, value in update_data.items():
            setattr(appointment, field, value)
            
        await db.commit()
        await db.refresh(appointment)
        return appointment

    @staticmethod
    async def cancel_appointment(db: AsyncSession, appointment_id: int) -> Appointment:
        appointment = await AppointmentService.get_appointment(db, appointment_id)
        appointment.status = AppointmentStatus.CANCELLED
        await db.commit()
        await db.refresh(appointment)
        return appointment

    @staticmethod
    async def delete_appointment(db: AsyncSession, appointment_id: int) -> None:
        appointment = await AppointmentService.get_appointment(db, appointment_id)
        await db.delete(appointment)
        await db.commit()

    @staticmethod
    async def is_doctor_available(
        db: AsyncSession,
        doctor_id: int,
        start_time: datetime,
        end_time: datetime,
        exclude_appointment_id: Optional[int] = None
    ) -> bool:
        day_of_week = start_time.weekday()
        start_time_str = start_time.strftime("%H:%M")
        end_time_str = end_time.strftime("%H:%M")
        
        availability = await db.execute(
            select(DoctorAvailability)
            .where(
                and_(
                    DoctorAvailability.doctor_id == doctor_id,
                    DoctorAvailability.day_of_week == day_of_week,
                    DoctorAvailability.is_available == True,
                    DoctorAvailability.start_time <= start_time_str,
                    DoctorAvailability.end_time >= end_time_str
                )
            )
        )
        
        if not availability.scalar():
            return False
            
        return True

    @staticmethod
    async def has_conflicting_appointment(
        db: AsyncSession,
        doctor_id: int,
        start_time: datetime,
        end_time: datetime,
        exclude_appointment_id: Optional[int] = None
    ) -> bool:
        query = select(Appointment).where(
            and_(
                Appointment.doctor_id == doctor_id,
                Appointment.status != AppointmentStatus.CANCELLED,
                or_(
                    and_(
                        Appointment.scheduled_time <= start_time,
                        Appointment.end_time > start_time
                    ),
                    and_(
                        Appointment.scheduled_time < end_time,
                        Appointment.end_time >= end_time
                    ),
                    and_(
                        Appointment.scheduled_time >= start_time,
                        Appointment.end_time <= end_time
                    )
                )
            )
        )
        
        if exclude_appointment_id:
            query = query.where(Appointment.id != exclude_appointment_id)
            
        result = await db.execute(query)
        return bool(result.scalars().first())