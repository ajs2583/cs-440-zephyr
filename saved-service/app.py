from flask import Flask, request, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user
from datetime import datetime

app = Flask(__name__)

# Initialize the database
db = SQLAlchemy(app)

# Create the database tables
@app.before_first_request
def create_tables():
    db.create_all()

class FlightDeal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    departure_airport = db.Column(db.String(10), nullable=False)
    destination_airport = db.Column(db.String(10), nullable=False)
    departure_date = db.Column(db.Date, nullable=False)
    price = db.Column(db.Float, nullable=False)
    booking_link = db.Column(db.String(500), nullable=False)

    search = db.relationship("User", backref="deal")

    def __repr__(self):
        return f"<FlightDeal {self.departure_airport} {self.destination_airport}, {self.price}, {self.user_id}>"

@app.route('/add_deal', methods=['POST'])
def add_deal():
    listOfData = request.url.split("add_deal?flight=")
    listOfData = listOfData[1].replace('{','').replace('}','').replace('\'', '').replace('+','').split(',')
    print(listOfData)
    rawDealList = []
    for each_data in listOfData:
        key, value = each_data.split(':', 1)
        print(key, value)
        rawDealList.append(value)
    
    departure = rawDealList[0]
    destination = rawDealList[1]
    departure_date = rawDealList[2]
    price = rawDealList[3]
    link = rawDealList[4]

    if len(departure) != 3 or len(destination) != 3:
        # Render the home page with an error message if the IATA code is invalid
        flash("There was an error with airport IATA codes", category="error")
        return render_template("index.html", user=current_user)
    date, time = departure_date.split('T')
    date = date.split('-')
    time = time.split(':')
    departure_date = datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2]))
    price = float(price)    
    if link == "None":
        link = ""
    

    new_deal = FlightDeal(
        user_id = current_user.id, 
        departure_airport = departure, 
        destination_airport = destination, 
        departure_date = departure_date, 
        price = price, 
        booking_link = link, 
    )
    db.session.add(new_deal)
    db.session.commit()

    flash('Deal added successfully!', category='success')

    return render_template("index.html", user=current_user)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5003)