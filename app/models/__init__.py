# app/models/__init__.py
from .base import Base, BaseModel  # This should now work
from .user import User
from .patient import Patient
from .doctor import Doctor
from .appointment import Appointment
from .medical_record import MedicalRecord

__all__ = [
    'Base',
    'BaseModel',
    'User',
    'Patient',
    'Doctor',
    'Appointment',
    'MedicalRecord'
]