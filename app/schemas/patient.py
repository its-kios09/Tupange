from datetime import date
from pydantic import BaseModel
from typing import Optional

class PatientBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    gender: str
    phone_number: str
    address: Optional[str] = None
    insurance_number: Optional[str] = None
    insurance_provider: Optional[str] = None

class PatientCreate(PatientBase):
    user_id: int

class PatientUpdate(PatientBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    insurance_number: Optional[str] = None
    insurance_provider: Optional[str] = None

class PatientProfileUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None

    class Config:
        from_attributes = True

class Patient(PatientBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True 