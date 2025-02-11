from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .views import views  # Correct relative import
# from flask_login import LoginManager
from os import path
from config import Config  # Import the new config file

# Initialize Flask extensions
migrate = Migrate()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Load settings from config.py

    db.init_app(app)
    migrate.init_app(app, db)

    from .views import views
    # from .auth import auth

    # Register blueprints
    app.register_blueprint(views, url_prefix='/')
    # app.register_blueprint(auth, url_prefix='/')

    # Initialize database before returning the app
    create_database(app)

    # # Set up login manager
    # login_manager = LoginManager()
    # login_manager.login_view = 'auth.login'
    # login_manager.init_app(app)

    return app  # Return the configured Flask app

# Create database if it does not exist
def create_database(app):
    db_path = path.join("instance", "zephyr.db")
    if not path.exists(db_path):
        with app.app_context():
            db.create_all()
            print('Created Database! 🎉')
