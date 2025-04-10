from pydantic import BaseModel
from typing import Optional

class DoctorBase(BaseModel):
    first_name: str
    last_name: str
    specialization: str
    phone_number: str
    bio: Optional[str] = None

class DoctorCreate(DoctorBase):
    user_id: int

class DoctorUpdate(DoctorBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    specialization: Optional[str] = None
    phone_number: Optional[str] = None
    bio: Optional[str] = None

class DoctorProfileUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    bio: Optional[str] = None

    class Config:
        from_attributes = True

class DoctorAvailabilityBase(BaseModel):
    day_of_week: int
    start_time: str
    end_time: str
    is_available: bool = True

class DoctorAvailabilityCreate(DoctorAvailabilityBase):
    doctor_id: int

# Add this new schema for availability updates
class DoctorAvailabilityUpdate(BaseModel):
    day_of_week: Optional[int] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    is_available: Optional[bool] = None

    class Config:
        from_attributes = True

class DoctorAvailability(DoctorAvailabilityBase):
    id: int
    doctor_id: int
    
    class Config:
        from_attributes = True

class Doctor(DoctorBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True