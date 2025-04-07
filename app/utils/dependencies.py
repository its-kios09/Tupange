from typing import Generator
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from app.database import get_db
from app.services.auth import get_current_active_user
from app.models.user import User

async def get_db_session() -> Generator:
    async with get_db() as session:
        yield session

async def get_current_patient(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db_session)
):
    if not current_user.patient:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user is not a patient"
        )
    return current_user.patient

async def get_current_doctor(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db_session)
):
    if not current_user.doctor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user is not a doctor"
        )
    return current_user.doctor