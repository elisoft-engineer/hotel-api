from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv
from core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)

Base = declarative_base()