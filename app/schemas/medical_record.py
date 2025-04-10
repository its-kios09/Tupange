from pydantic import BaseModel
from typing import Optional, List

class MedicalRecordBase(BaseModel):
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    prescription: Optional[str] = None
    notes: Optional[str] = None

class MedicalRecordCreate(MedicalRecordBase):
    patient_id: int
    appointment_id: Optional[int] = None

class MedicalRecordUpdate(MedicalRecordBase):
    pass

class MedicalRecord(MedicalRecordBase):
    id: int
    patient_id: int
    appointment_id: Optional[int] = None

    class Config:
        orm_mode = True
    