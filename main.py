from os import path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_standalone_docs import StandaloneDocs

from api import auth as auth_api
from api import menu as menu_api
from api import messages as message_api
from api import notifications as notification_api
from api import orders as order_api
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
