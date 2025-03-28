from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user



auth = Blueprint('auth', __name__)


# login routing
@auth.route('/login', methods=['GET', 'POST'])
def login():

    # check for post
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # search for the user trying to login with the email
        user = User.query.filter_by(email=email).first()
        # if we found the user
        if user:
            # if the password matches the hashed password in db
            if check_password_hash(user.password_hash, password):
                # notify log in successful
                flash('Logged in successfully!', category='success')

                # login user to flask_login
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            # otherwise the password was incorrect
            else:
                flash('Incorrect password, try again.', category='error')
        # otherwise email does not exist in the database
        else:
            flash("Email does not exist.", category='error')





    return render_template("login.html", user=current_user)

# logout routing
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# signup routing
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():

    # if the method is a post, grab all of the data
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()


        # first check if the email is already associated with an account
        if user:
            flash("Email already has an account", category='error')
        # then check if username is already associated with an account
        elif ( User.query.filter_by(name=username).first() ):
            flash("Username already has an acccount", category='error')
        # otherwise check data validity
        elif len(email) < 4:
            flash("Email must be greater than 3 characters.", category='error')
        elif len(username) < 2:
            flash("First name must be longer than 1 character.", category='error')
        elif len(password) < 7:
            flash("Password must be at least 7 characters.", category='error')
        else:
            # add user to the database
                    # hash the password to ensure data security using sha256 method
            new_user = User(email=email, name=username, password_hash=generate_password_hash(username, method='pbkdf2:sha256'))
            # add user
            db.session.add(new_user)
            # commit user to db
            db.session.commit()
 
            # login the user once account created
            login_user(new_user, remember=True)
            # alert user of account creation
            flash('Account created!', category='success')

            # send the user to the home page
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)