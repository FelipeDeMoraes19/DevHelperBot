import pytest
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager
from app.main import app
from app.config.database import AsyncSessionLocal, engine, Base, get_db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from app.config.database import Base


@pytest.fixture(scope="session")
async def db_engine():
    engine = create_async_engine(
        "postgresql+asyncpg://devhelper:secretpassword@postgres:5432/devhelper_test",
        echo=True,
        poolclass=NullPool
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest.fixture
async def db(db_engine):
    connection = await db_engine.connect()
    transaction = await connection.begin()
    session_maker = sessionmaker(
        bind=connection,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    session = session_maker()
    
    try:
        yield session
    finally:
        await session.close()
        await transaction.rollback()
        await connection.close()

@pytest.fixture
async def async_client(db):
    app.dependency_overrides[get_db] = lambda: db
    
    async with LifespanManager(app):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
        ) as client:
            yield client
    
    app.dependency_overrides.clear()