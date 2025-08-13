# core/config.py
from pydantic_settings import BaseSettings
from os import path, makedirs


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_LIFETIME: int
    DATABASE_URL: str

    BASE_DIR: str = path.dirname(path.dirname(path.abspath(__file__)))
    FILES_DIR: str = path.join(BASE_DIR, "files")
    MENU_DIR: str = path.join(FILES_DIR, "menu")
    MENU_IMAGES_DIR: str = path.join(MENU_DIR, "images")
    MENU_THUMBNAILS_DIR: str = path.join(MENU_DIR, "thumbnails")

    class Config:
        env_file = ".env.dev"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        makedirs(self.FILES_DIR, exist_ok=True)
        makedirs(self.MENU_DIR, exist_ok=True)
        makedirs(self.MENU_IMAGES_DIR, exist_ok=True)
        makedirs(self.MENU_THUMBNAILS_DIR, exist_ok=True)


settings = Settings()
