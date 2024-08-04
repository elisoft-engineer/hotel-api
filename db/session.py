from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from .base import engine
from typing import AsyncGenerator

"""
This file handles the database connection management during CRUD activities
"""

AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    with AsyncSession() as db:
        yield db
        