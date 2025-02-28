import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool

def get_database_url():
    if os.getenv("ENV") == "testing":
        return "postgresql+asyncpg://devhelper:secretpassword@postgres:5432/devhelper_test"
    return "postgresql+asyncpg://devhelper:secretpassword@postgres:5432/devhelper_db"

engine = create_async_engine(
    get_database_url(),
    echo=True,
    poolclass=NullPool if os.getenv("ENV") == "testing" else None
)

AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session