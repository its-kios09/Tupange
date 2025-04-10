import logging
from datetime import datetime
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.redis_client import redis_client
from app.models.appointment import Appointment
from app.config import settings

logger = logging.getLogger(__name__)

class NotificationService:
    @staticmethod
    async def send_appointment_confirmation(
        db: AsyncSession,
        appointment: Appointment
    ) -> None:
        # In a real implementation, this would send an email/SMS
        # Here we'll just log and store in Redis for demo purposes
        message = (
            f"Appointment confirmed for {appointment.scheduled_time} "
            f"with Dr. {appointment.doctor.last_name}"
        )
        
        # Store notification in Redis with 24h expiration
        await redis_client.setex(
            f"appointment:{appointment.id}:notification",
            settings.REDIS_CACHE_EXPIRE,
            message
        )
        
        logger.info(f"Sent appointment confirmation: {message}")

    @staticmethod
    async def send_appointment_reminder(
        db: AsyncSession,
        appointment: Appointment
    ) -> None:
        # Send reminder 1 hour before appointment
        message = (
            f"Reminder: You have an appointment in 1 hour "
            f"with Dr. {appointment.doctor.last_name}"
        )
        
        await redis_client.setex(
            f"appointment:{appointment.id}:reminder",
            settings.REDIS_CACHE_EXPIRE,
            message
        )
        
        logger.info(f"Sent appointment reminder: {message}")