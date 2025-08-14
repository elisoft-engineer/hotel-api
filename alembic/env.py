import asyncio
import os
import sys
from logging.config import fileConfig

import alembic_postgresql_enum
from dotenv import load_dotenv

from alembic import context

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_dotenv(os.path.join(BASE_DIR, ".env.dev"))

sys.path.append(BASE_DIR)

config = context.config

config.set_main_option("sqlalchemy.url", os.getenv('DATABASE_URL', ''))

from auth import models
from core.database import Base, engine
from menu import models
from messages import models
from notifications import models
from orders import models

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    async with engine.begin() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
