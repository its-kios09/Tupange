import asyncio
from pathlib import Path
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.config import settings
from app.services.auth import get_password_hash
from app.models.user import User
from app.database import Base
import logging

logger = logging.getLogger(__name__)

async def is_database_initialized(engine) -> bool:
    """Check if database has already been initialized"""
    try:
        async with engine.connect() as conn:
            result = await conn.execute(
                text("SELECT 1 FROM db_initialization LIMIT 1")
            )
            return bool(result.scalar())
    except Exception:
        return False

async def execute_sql_file(engine, file_path: Path):
    """Execute SQL commands from a file in a single transaction"""
    try:
        async with engine.begin() as conn:  # Use a transaction
            sql_content = file_path.read_text()
            # Split into individual statements and execute
            for statement in sql_content.split(';'):
                statement = statement.strip()
                if statement:  # Skip empty statements
                    await conn.execute(text(statement))
            logger.info("SQL file executed successfully")
    except Exception as e:
        logger.error(f"Error executing SQL file: {e}")
        raise

async def create_database():
    """Create the database if it doesn't exist"""
    temp_engine = create_async_engine(
        str(settings.DATABASE_URL).replace(f"/{settings.MYSQL_DATABASE}", ""),
        isolation_level="AUTOCOMMIT"
    )
    
    try:
        async with temp_engine.connect() as conn:
            await conn.execute(
                text(f"CREATE DATABASE IF NOT EXISTS {settings.MYSQL_DATABASE} "
                     f"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            )
            logger.info(f"Database {settings.MYSQL_DATABASE} created or already exists")
    except Exception as e:
        logger.error(f"Error creating database: {e}")
        raise
    finally:
        await temp_engine.dispose()

async def initialize_database_once():
    """Initialize database with SQL file only if not already initialized"""
    engine = create_async_engine(settings.DATABASE_URL)
    try:
        if await is_database_initialized(engine):
            logger.info("Database already initialized - skipping SQL execution")
            return
        
        sql_file = Path(__file__).parent.parent / "db" / "initial_setup_database.sql"
        if not sql_file.exists():
            raise FileNotFoundError(f"SQL file not found at {sql_file}")
        
        logger.info("First-time database initialization starting")
        await execute_sql_file(engine, sql_file)
        logger.info("Database initialized successfully from SQL file")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise
    finally:
        await engine.dispose()

async def create_superuser():
    """Create initial superuser if it doesn't exist"""
    engine = create_async_engine(settings.DATABASE_URL)
    async with AsyncSession(engine) as db:
        try:
            existing_user = await db.execute(
                text("SELECT id FROM users WHERE email = :email"),
                {"email": settings.FIRST_SUPERUSER}
            )
            if existing_user.scalar():
                logger.info("Superuser already exists")
                return
            
            hashed_password = get_password_hash(settings.FIRST_SUPERUSER_PASSWORD)
            superuser = User(
                email=settings.FIRST_SUPERUSER,
                hashed_password=hashed_password,
                is_active=True,
                is_superuser=True
            )
            db.add(superuser)
            await db.commit()
            logger.info(f"Superuser {settings.FIRST_SUPERUSER} created")
        except Exception as e:
            logger.error(f"Error creating superuser: {e}")
            await db.rollback()
            raise

async def init_db():
    """Initialize database with all required components"""
    await create_database()
    await initialize_database_once()
    await create_superuser()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(init_db())