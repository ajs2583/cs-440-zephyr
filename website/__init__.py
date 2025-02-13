from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .views import views  # Correct relative import
# from flask_login import LoginManager
from os import path
from settings import Config  # Import the new config file

# Initialize Flask extensions
migrate = Migrate()  # Initialize Flask-Migrate
db = SQLAlchemy()  # Initialize SQLAlchemy

def create_app():
    
    # Create a Flask application instance
    app = Flask(__name__)  
    
    # Set the secret key for session management
    app.config['SECRET_KEY'] = 'super duper secret key'  
    
    # Load configuration from Config object
    app.config.from_object(Config)  
    
    # Initialize SQLAlchemy with the app
    db.init_app(app)
     # Initialize Flask-Migrate with the app and database  
    migrate.init_app(app, db) 

    # Import views blueprint
    from .views import views  
    # from .auth import auth  # Import auth blueprint (commented out)

    # Register views blueprint with the app
    app.register_blueprint(views, url_prefix='/')  
    # app.register_blueprint(auth, url_prefix='/')  # Register auth blueprint with the app (commented out)

    create_database(app)  # Create the database if it does not exist

    # login_manager = LoginManager()  # Initialize LoginManager (commented out)
    # login_manager.login_view = 'auth.login'  # Set the login view for LoginManager (commented out)
    # login_manager.init_app(app)  # Initialize LoginManager with the app (commented out)

    # Return the configured Flask app
    return app  

def create_database(app):
    # Define the database path
   db_path = path.join("instance", "zephyr.db")
   # Check if local DB should be used and if it doesn't exist  
   if Config.USE_LOCAL_DB and not path.exists(db_path):  
        with app.app_context():
            # Create all database tables
            db.create_all()
            # Print success message  
            print('Created Local SQLite Database! 🎉')  
