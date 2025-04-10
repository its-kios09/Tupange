import asyncio
from pathlib import Path
from sqlalchemy import text
from app.config import settings
from app.database import get_engine, get_async_session_maker, Base
import logging
from app.models.user import User
from app.services.auth import get_password_hash

logger = logging.getLogger(__name__)

async def is_database_initialized(engine) -> bool:
    try:
        async with engine.connect() as conn:
            result = await conn.execute(
                text("""
                    SELECT COUNT(*) FROM information_schema.tables 
                    WHERE table_schema = :database AND table_name = 'users'
                """),
                {"database": settings.MYSQL_DATABASE}
            )
            return bool(result.scalar())
    except Exception as e:
        logger.warning(f"Initialization check failed: {e}")
        return False

async def execute_sql_file(engine, file_path: Path):
    try:
        async with engine.begin() as conn:
            sql_content = file_path.read_text()
            for statement in sql_content.split(';'):
                if statement.strip():
                    try:
                        await conn.execute(text(statement))
                    except Exception as e:
                        logger.warning(f"Statement failed (might be harmless): {e}")
            logger.info("✅ SQL file executed successfully")
    except Exception as e:
        logger.error(f"Error executing SQL file: {e}")
        raise

async def create_superuser():
    async_session = get_async_session_maker()
    async with async_session() as db:
        try:
            existing_user = await User.get_by_email(db, settings.FIRST_SUPERUSER)
            if not existing_user:
                hashed_password = get_password_hash(settings.FIRST_SUPERUSER_PASSWORD)
                superuser = User(
                    email=settings.FIRST_SUPERUSER,
                    hashed_password=hashed_password,
                    is_active=True,
                    is_superuser=True,
                    role="admin"
                )
                db.add(superuser)
                await db.commit()
                logger.info(f"✅ Superuser {settings.FIRST_SUPERUSER} created")
            else:
                logger.info("✅ Superuser already exists")
        except Exception as e:
            logger.error(f"Error creating superuser: {e}")
            await db.rollback()
            raise

async def init_db():
    engine = get_engine()
    async_session = get_async_session_maker()
    
    sql_file = Path(__file__).parent.parent / "db" / "initial_setup_database.sql"
    
    if sql_file.exists():
        if not await is_database_initialized(engine):
            logger.info("First-time database initialization starting")
            try:
                # Create tables using SQLAlchemy metadata
                async with engine.begin() as conn:
                    await conn.run_sync(Base.metadata.create_all)
                
                # Execute the SQL file for additional setup
                await execute_sql_file(engine, sql_file)
                logger.info("✅ Database initialized successfully")
            except Exception as e:
                logger.error(f"8Database initialization failed: {e}")
                raise
    
    # Create superuser using proper session
    await create_superuser()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(init_db())