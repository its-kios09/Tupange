from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

class PatientNotFoundException(HTTPException):
    def __init__(self, patient_id: int):
        super().__init__(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Patient with id {patient_id} not found"
        )
class DoctorNotFoundException(HTTPException):
    def __init__(self, doctor_id: int):
        super().__init__(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Doctor with id {doctor_id} not found"
        )
class AppointmentNotFoundException(HTTPException):
    def __init__(self, appointment_id: int):
        super().__init__(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Appointment with id {appointment_id} not found"
        )
class MedicalRecordNotFoundException(HTTPException):
    def __init__(self, record_id: int):
        super().__init__(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Medical record with id {record_id} not found"
        )

class DoctorNotAvailableException(HTTPException):
    def __init__(self, doctor_id: int):
        super().__init__(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = f"Doctor with id {doctor_id} is not available at the requested time"
        )

class AppointmentConflictException(HTTPException):
    def __init__(self, doctor_id: int):
        super().__init__(
            status_code = status.HTTP_409_CONFLICT,
            detail = f"Appointment time conflict with doctor with an existing appointment"
        )

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
    
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )

async def custom_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": str(exc)},
    )
    