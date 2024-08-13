from fastapi import FastAPI
from db.base import engine
from db.session import AsyncSessionLocal
from db.models import menu as menu_models, messages as message_models, notifications as notification_models, \
    orders as order_models, users as user_models
from api import menu as menu_api, messages as message_api, notifications as notification_api, \
    orders as order_api, users as user_api
from core.config import settings
from os import path, getenv
from dotenv import load_dotenv


load_dotenv(path.join(settings.BASE_DIR, ".env"))


async def create_all_tables_async():
    async with AsyncSessionLocal() as async_session:
        async_session.run_sync(menu_models.Base.metadata.create_all(bind=engine))
        async_session.run_sync(message_models.Base.metadata.create_all(bind=engine))
        async_session.run_sync(notification_models.Base.metadata.create_all(bind=engine))
        async_session.run_sync(order_models.Base.metadata.create_all(bind=engine))
        async_session.run_sync(user_models.Base.metadata.create_all(bind=engine))


app = FastAPI(debug=bool(getenv("DEBUG")))


app.include_router(menu_api.router)
app.include_router(message_api.router)
app.include_router(notification_api.router)
app.include_router(order_api.router)
app.include_router(user_api.router)
