from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from core.conf import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)

Base = declarative_base()

AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession = AsyncSessionLocal()
    try:
        yield session
    finally:
        await session.close()
