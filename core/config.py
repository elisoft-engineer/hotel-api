from dotenv import load_dotenv
from os import getenv, path, makedirs

load_dotenv()

"""
This file handles the app configuration such as the database uri, file system
management, e.t.c
"""

class Settings:
    SECRET_KEY: str = getenv("SECRET_KEY")
    ALGORITHM: str = getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    DATABASE_URL: str = getenv('DATABASE_URL')
    
    BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))
    FILES_DIR = path.join(BASE_DIR, "files")
    MENU_DIR = path.join(FILES_DIR, "menu")

    makedirs(FILES_DIR, exist_ok=True)
    makedirs(MENU_DIR, exist_ok=True)


settings = Settings()
