from flask import Flask, jsonify, request, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, current_user, LoginManager
import os
import logging

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://auth_user:auth_password@db:5432/auth_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.logger.info(f"Connecting to database at {app.config['SQLALCHEMY_DATABASE_URI']}")
app.secret_key = os.getenv("SECRET_KEY", "fallback_key")

# Initialize the database
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id)) 

# Define a User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<User {self.name} ({self.email})>"

# Create the database tables
@app.before_first_request
def create_tables():
    db.create_all()

# Sample route to add a user
@app.route('/sign-up', methods=['POST', 'GET'])
def register_user():
    if request.method == 'GET':
        return render_template("sign_up.html", user=current_user)
    #data = request.json
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    
    # Check if user already exists
    user = User.query.filter_by(name=username).first()
    if user:
        return jsonify({"error": "User already exists"}), 400

    # Create a new user
    new_user = User(email=email, name=username, password_hash=generate_password_hash(password, method='pbkdf2:sha256'))
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201

@app.route('/login', methods=['GET', 'POST'])
def login():
    # check for post
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        app.logger.setLevel(logging.DEBUG)
        # search for the user trying to login with the email
        user = User.query.filter_by(email=email).first()
        app.logger.info(f"📥 Received data: {user}")
        # if we found the user
        if user:
            # if the password matches the hashed password in db
            if check_password_hash(user.password_hash, password):
                # login user to flask_login
                login_user(user, remember=True)
                flash("Login Success", category='error')
                return redirect("http://gateway:5000")
            # otherwise the password was incorrect
            else:
                flash("Password was incorrect", category='error')
        # otherwise email does not exist in the database
        else:
            flash("Email does not exist", category='error')
    return render_template("login.html", user=current_user)



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
