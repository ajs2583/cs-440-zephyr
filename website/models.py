from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<User {self.name} ({self.email})>"

class FlightSearch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    departure_airport = db.Column(db.String(10), nullable=False)
    destination_country = db.Column(db.String(10))
    departure_date = db.Column(db.Date, nullable=False)
    max_budget = db.Column(db.Float)

    user = db.relationship("User", backref="searchquery")

    def __repr__(self):
        return f"<FlightSearch {self.departure_airport} {self.destination_airport}, {self.max_budget}, {self.user_id}"

class FlightDeal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    departure_airport = db.Column(db.String(10), nullable=False)
    destination_airport = db.Column(db.String(10), nullable=False)
    departure_date = db.Column(db.Date, nullable=False)
    price = db.Column(db.Float, nullable=False)
    booking_link = db.Column(db.String(500), nullable=False)

    search = db.relationship("User", backref="deal")

    def __repr__(self):
        return f"<FlightDeal {self.departure_airport} {self.destination_airport}, {self.price}, {self.user_id}>"