from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

class FlightSearch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    departure_airport = db.Column(db.String(10), nullable=False)
    destination_airport = db.Column(db.String(10))
    date_range_start = db.Column(db.Date, nullable=False)
    date_range_end = db.Column(db.Date, nullable=False)
    max_budget = db.Column(db.Float)

class FlightDeal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    search_id = db.Column(db.Integer, db.ForeignKey("flight_search.id"), nullable=False)
    departure_airport = db.Column(db.String(10), nullable=False)
    destination_airport = db.Column(db.String(10), nullable=False)
    departure_date = db.Column(db.Date, nullable=False)
    price = db.Column(db.Float, nullable=False)
    booking_link = db.Column(db.String(500), nullable=False)
