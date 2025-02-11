from os import getenv
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = getenv("SECRET_KEY", "super duper secret key")

    # USE THIS FOR LOCAL TESTING (SQLite)
    LOCAL_DB = f"sqlite:///zephyr.db"

    # USE THIS FOR SERVER (Production Database from .env)
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URL", LOCAL_DB)
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
