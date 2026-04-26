from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.configs.environment import get_environment_settings


env = get_environment_settings()

DATABASE_URL = (
    f"{env.DATABASE_DIALECT}://{env.DATABASE_USERNAME}:{env.DATABASE_PASSWORD}"
    f"@{env.DATABASE_HOST}:{env.DATABASE_PORT}/{env.DATABASE_NAME}"
)

Engine = create_async_engine(
    DATABASE_URL, 
    echo=env.DEBUG_MODE,
    future=True
)

AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=Engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db_connection():
    async with AsyncSessionLocal() as session:
        yield session