from os import getenv
from dotenv import load_dotenv

# Always load .env to ensure environment variables are available
load_dotenv()

class Config:
    
    # Secret Key (used for session security, CSRF protection, etc.)
    SECRET_KEY = getenv("SECRET_KEY")

    # Pull Database URLs from .env
    SQLITE_DATABASE_URL = getenv("SQLITE_DATABASE_URL")  # Local SQLite
    POSTGRES_DATABASE_URL = getenv("POSTGRES_DATABASE_URL")  # Render PostgreSQL
    
    # Pull Boolean for use of local or server testing from .env
    USE_LOCAL_DB = getenv("USE_LOCAL_DB", "False").strip().lower() in ("true", "1", "t")
    
    # If true use local 
    if USE_LOCAL_DB:
        print("🔹 Using Local SQLite Database")
        # Use SQLite
        SQLALCHEMY_DATABASE_URI = SQLITE_DATABASE_URL 
    # If false use server 
    else:
        print("🚀 Using Render PostgreSQL Database")
        # Use PosgreSQL
        SQLALCHEMY_DATABASE_URI = POSTGRES_DATABASE_URL
        
        

    # SQLAlchemy settings
    # Disables the modification tracking system, which consumes extra memory.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # SQLAlchemy engine options
    # Enables the 'pool_pre_ping' option to prevent connection pool issues.
        # This sends a simple query to the database before using a connection from the pool,
        # ensuring that the connection is still valid and preventing 'connection drop' issues.
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}  

    
    
