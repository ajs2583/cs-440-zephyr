from flask import Blueprint, render_template, request, jsonify
from .services import get_airport_suggestions, get_flight_deals

# Create a Blueprint named 'views' for organizing routes
views = Blueprint("views", __name__)

# Route for the home page
@views.route("/", methods=["GET"])
def home():
    # Render the home page template with an empty list of airports
    return render_template("index.html", airports=[])

# Route to get airport suggestions based on a query
@views.route("/get_airports", methods=["GET"])
def get_airports():
    # Get the query parameter 'q' from the request
    query = request.args.get("q", "")
    # Fetch airport suggestions using the query
    airports = get_airport_suggestions(query)
    # Return the suggestions as a JSON response
    return jsonify(airports)

# Route to search for flight deals
@views.route("/search_flights", methods=["POST"])
def search_flights():
    # Get form data from the request
    airport_full = request.form.get("airport")
    date = request.form.get("date")
    max_price = request.form.get("price")
    dest_country = request.form.get("countries")

    # Check if required fields are filled
    if not airport_full or not date:
        # Render the home page with an error message if fields are missing
        return render_template("index.html", error="Please fill in all fields.")

    # Extract IATA code from the airport string safely
    airport_code = airport_full.split("(")[-1].replace(")", "").strip()

    # extract the country code good
    dest_country = dest_country.split("(")[-1].replace(")", "").strip()
    
    # Ensure the extracted IATA code is valid (3 characters long)
    if len(airport_code) != 3:
        # Render the home page with an error message if the IATA code is invalid
        return render_template("index.html", error="Invalid airport selection.")

    #! Debugging: Print extracted airport code, date, and max price
    print(f"Extracted Airport Code: {airport_code}")
    print(f"Using Date: {date}")
    print(f"Using Max Price: {max_price}")
    print(f"Using Dest Country: {dest_country}")

    # Fetch flight deals using the extracted IATA code, date, and max price
    flights = get_flight_deals(airport_code, date, int(max_price), dest_country)
    # Render the home page with the list of flight deals
    return render_template("index.html", flights=flights)
