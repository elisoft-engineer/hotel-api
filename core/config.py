from dotenv import load_dotenv
import os

class Settings:
    DATABASE_URL: str = os.getenv('DATABASE_URL')

settings = Settings()