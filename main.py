from os import path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_standalone_docs import StandaloneDocs

from auth import routes as auth_routes
from menu import routes as menu_routes
from messages import routes as message_routes
from notifications import routes as notification_routes
from orders import routes as order_routes
from core.conf import settings

load_dotenv(path.join(settings.BASE_DIR, ".env"))

app = FastAPI()
StandaloneDocs(app=app, with_google_fonts=True)


app.include_router(auth_routes.router)
app.include_router(menu_routes.router)
app.include_router(order_routes.router)
app.include_router(message_routes.router)
app.include_router(notification_routes.router)
