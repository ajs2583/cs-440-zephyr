from flask import Blueprint

views = Blueprint("views", __name__)  

@views.route("/")
def home():
    return {"message": "Zephyr Flight Tracker is Running!"}
