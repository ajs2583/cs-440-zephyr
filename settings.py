import os
from dotenv import load_dotenv

# Always load .env to ensure environment variables are available
load_dotenv()

class Config:
    # Secret Key (used for session security, CSRF protection, etc.)
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Database URLs
    SQLITE_DATABASE_URL = os.getenv("SQLITE_DATABASE_URL")  # Local SQLite
    POSTGRES_DATABASE_URL = os.getenv("POSTGRES_DATABASE_URL")  # Render PostgreSQL

    '''
    TRUE FOR LOCAL TESTING
    FALSE FOR SERVER TESTING
    '''
    SQLALCHEMY_DATABASE_URI = SQLITE_DATABASE_URL
    # USE_LOCAL_DB = os.getenv("USE_LOCAL_DB", "False").strip().lower() in ("true", "1", "t")
    # if USE_LOCAL_DB:
    #     print("🔹 Using Local SQLite Database")
    #     SQLALCHEMY_DATABASE_URI = SQLITE_DATABASE_URL # Use SQLite
    # else:
    #     print("🚀 Using Render PostgreSQL Database")
    #     SQLALCHEMY_DATABASE_URI = POSTGRES_DATABASE_URL
        
        

    # SQLAlchemy settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}  # Prevents connection drop issues

    
    
