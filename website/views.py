from flask import Blueprint, render_template, request, jsonify, redirect, flash
from .services import get_airport_suggestions, get_flight_deals
from flask_login import login_required, current_user
from .models import User, FlightSearch, FlightDeal
from . import db
from datetime import datetime

# Create a Blueprint named 'views' for organizing routes
views = Blueprint("views", __name__)

# Route for the home page
@views.route("/", methods=["GET"])
@login_required
def home():
    # Render the home page template with an empty list of airports
    return render_template("index.html", airports=[], user=current_user)

# Route to get airport suggestions based on a query
@views.route("/get_airports", methods=["GET"])
@login_required
def get_airports():
    # Get the query parameter 'q' from the request
    query = request.args.get("q", "")
    # Fetch airport suggestions using the query
    airports = get_airport_suggestions(query)
    # Return the suggestions as a JSON response
    return jsonify(airports)

# Route to search for flight deals
@views.route("/search_flights", methods=["POST"])
@login_required
def search_flights():
    # Get form data from the request
    # Airport
    airport_full = request.form.get("airport")
    # Date
    date = request.form.get("date")
    # Price
    max_price = request.form.get("price")
    # Destination country 
    dest_country = request.form.get("countries")

    # Check if required fields are filled
    if not airport_full or not date:
        # Render the home page with an error message if fields are missing
        flash("Please fill in all fields.", category="error")
        return render_template("index.html",  user=current_user)

    # Extract IATA code from the airport string safely
    airport_code = airport_full.split("(")[-1].replace(")", "").strip()

    # extract the country code good
    dest_country = dest_country.split("(")[-1].replace(")", "").strip()
    
    # Ensure the extracted IATA code is valid (3 characters long)
    if len(airport_code) != 3:
        # Render the home page with an error message if the IATA code is invalid
        flash("Invalid airport selection.", category="error")
        return render_template("index.html", user=current_user)

    #! Debugging: Print extracted airport code, date, and max price
    print(f"Extracted Airport Code: {airport_code}")
    print(f"Using Date: {date}")
    print(f"Using Max Price: {max_price}")
    print(f"Using Dest Country: {dest_country}")

    # Fetch flight deals using the extracted IATA code, date, and max price
    flights = get_flight_deals(airport_code, date, int(max_price), dest_country)
    new_date = date.split('-')
    new_date = datetime(int(new_date[0]), int(new_date[1]), int(new_date[2]), 0, 0, 0) 
    new_search = FlightSearch(
        user_id = current_user.id, 
        departure_airport = airport_code, 
        destination_country = dest_country, 
        departure_date = new_date, 
        max_budget = float(max_price), 
    )
    db.session.add(new_search)
    db.session.commit()

    # Render the home page with the list of flight deals
    return render_template("index.html", flights=flights, user=current_user)

@views.route("/book/<offer_id>", methods=["GET"])
@login_required
def book_flight(offer_id):
    # Check if the offer_id is a full URL
    if offer_id.startswith("http"):
        # Redirect to the full URL if it is
        return redirect(offer_id)
    else:
        # Construct the booking URL using the offer_id
        booking_url = f"https://www.amadeus.com/book/{offer_id}"
        # Redirect to the constructed booking URL
        return redirect(booking_url)
    
@views.route('/add_deal', methods=['POST'])
@login_required
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

@views.route('/profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def view_profile(user_id):
    user_profile = User.query.get_or_404(user_id)
    is_own_profile = current_user.id == user_id

    return_deals = []
    return_searches = []
    deal_list = FlightDeal.query.all()
    search_list = FlightSearch.query.all()

    for each_deal in deal_list:
        if each_deal.user_id == current_user.id:
            return_deals.append(each_deal)
    for each_search in search_list:
        if each_search.user_id == current_user.id:
            return_searches.append(each_search)
    return render_template(
        'profile.html',
        user_profile=user_profile,
        is_own_profile=is_own_profile,
        user=current_user,
        flightdeals = return_deals,
        flightsearches = return_searches
    )