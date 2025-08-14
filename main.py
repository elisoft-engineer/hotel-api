from os import path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_standalone_docs import StandaloneDocs

from api import auth as auth_api
from menu import routes as menu_api
from messages import routes as message_api
from notifications import routes as notification_api
from orders import routes as order_api
from api import users as user_api
from core.config import settings

load_dotenv(path.join(settings.BASE_DIR, ".env"))

app = FastAPI()
StandaloneDocs(app=app, with_google_fonts=True)


app.include_router(auth_api.router)
app.include_router(user_api.router)
app.include_router(menu_api.router)
app.include_router(order_api.router)
app.include_router(message_api.router)
app.include_router(notification_api.router)
