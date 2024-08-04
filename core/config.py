from dotenv import load_dotenv
import os


"""
This file handles the app configuration such as the database uri, file system
management, e.t.c
"""

class Settings:
    DATABASE_URL: str = os.getenv('DATABASE_URL')


settings = Settings()
