from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from core.config import settings

"""
Creation of the asynchronous database engine happens from this file. The Base is the used in the db models as the 
abstract model.
"""

engine = create_async_engine(settings.DATABASE_URL, echo=True)

Base = declarative_base()

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from .base import engine

"""
This file handles the database connection management during CRUD activities
"""

AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as db:
        yield db
