from fastapi import FastAPI
from fastapi_standalone_docs import StandaloneDocs
from db.base import engine
from db.session import AsyncSessionLocal
from db.models import menu as menu_models, messages as message_models, notifications as notification_models, \
    orders as order_models, users as user_models
from api import menu as menu_api, messages as message_api, notifications as notification_api, \
    orders as order_api, users as user_api, auth as auth_api
from core.config import settings
from os import path
from dotenv import load_dotenv

load_dotenv(path.join(settings.BASE_DIR, ".env"))

app = FastAPI(docs_url="/swagger", redoc_url=None)
StandaloneDocs(app=app)


app.include_router(auth_api.router)
app.include_router(user_api.router)
app.include_router(menu_api.router)
app.include_router(order_api.router)
app.include_router(message_api.router)
app.include_router(notification_api.router)
