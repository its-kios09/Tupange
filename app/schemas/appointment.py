from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from enum import Enum

class AppointmentStatus(str, Enum):
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    scheduled_time: datetime
    end_time: datetime
    status: AppointmentStatus = AppointmentStatus.SCHEDULED
    reason: Optional[str] = None
    notes: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(BaseModel):
    scheduled_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[AppointmentStatus] = None
    reason: Optional[str] = None
    notes: Optional[str] = None

# Add this new schema for status updates
class AppointmentStatusUpdate(BaseModel):
    status: AppointmentStatus

class AppointmentSlot(BaseModel):
    start_time: datetime
    end_time: datetime
    doctor_id: int

class Appointment(AppointmentBase):
    id: int

    class Config:
        from_attributes = True
        use_enum_values = True