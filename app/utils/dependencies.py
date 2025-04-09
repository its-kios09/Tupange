# database.py
import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import text
from app.config import settings
import logging

__all__ = [
    'Base',
    'init_db_engine',
    'get_engine',
    'get_async_session_maker',
    'get_db',
    'check_db_connection',
    'create_database'
]

logger = logging.getLogger(__name__)

Base = declarative_base()

# Initialize these as None at module level
_engine = None
_async_session_maker = None

async def create_database():
    """Create the database if it doesn't exist."""
    # Create a temporary engine without database name
    temp_url = settings.DATABASE_URL.replace(f"/{settings.MYSQL_DATABASE}", "")
    temp_engine = create_async_engine(
        temp_url,
        pool_pre_ping=True,
        echo=settings.DEBUG if hasattr(settings, 'DEBUG') else False
    )
    
    try:
        async with temp_engine.connect() as conn:
            # Create database if it doesn't exist
            await conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {settings.MYSQL_DATABASE}"))
            logger.info(f"Database {settings.MYSQL_DATABASE} created or already exists")
    except Exception as e:
        logger.error(f"Error creating database: {e}")
        raise
    finally:
        await temp_engine.dispose()

async def init_db_engine():
    global _engine, _async_session_maker
    if _engine is None:
        try:
            _engine = create_async_engine(
                settings.DATABASE_URL,
                pool_pre_ping=True,
                echo=settings.DEBUG if hasattr(settings, 'DEBUG') else False
            )
            # Test the connection
            async with _engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            
            _async_session_maker = async_sessionmaker(_engine, expire_on_commit=False)
            return _engine
        except Exception as e:
            logger.warning(f"Database connection failed: {e}")
            if "Unknown database" in str(e):
                await create_database()
                return await init_db_engine()  # Try again after creating database
            raise  # Re-raise other errors

def get_engine():
    if _engine is None:
        raise RuntimeError("Database engine not initialized. Call init_db_engine() first.")
    return _engine

def get_async_session_maker():
    if _async_session_maker is None:
        raise RuntimeError("Async session maker not initialized. Call init_db_engine() first.")
    return _async_session_maker

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async_session = get_async_session_maker()
    async with async_session() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()

async def check_db_connection() -> bool:
    engine = get_engine()
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
            return True
    except Exception as e:
        logger.error(f"Database connection check failed: {e}")
        return False