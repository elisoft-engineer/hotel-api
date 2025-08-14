from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from core.config import settings

"""
Creation of the asynchronous database engine happens from this file. The Base is the used in the db models as the 
abstract model.
"""

engine = create_async_engine(settings.DATABASE_URL, echo=True)

Base = declarative_base()
