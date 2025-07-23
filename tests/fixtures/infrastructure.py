import pytest
import pytest_asyncio
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.settings import Settings
from app.infrastructure.database.database import Base


@pytest.fixture
def settings():
    return Settings()


engine = create_async_engine(
    url='postgresql+asyncpg://user:password@127.0.0.1:5432/pomodoro-test',
    future=True,
    echo=True,
    pool_pre_ping=True,
    poolclass=NullPool
)


AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False,
)


@pytest_asyncio.fixture(autouse=True, scope='session')
async def init_models(event_loop):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope='session')
async def get_db_session() -> AsyncSession:
    return AsyncSessionFactory()
