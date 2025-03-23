from flask import Flask, request, render_template, flash, jsonify 
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user
from datetime import datetime
from amadeus import Client, ResponseError
from os import getenv
import concurrent.futures
import time

amadeus = Client(
    client_id=getenv("AMADEUS_API_KEY"),
    client_secret=getenv("AMADEUS_API_SECRET")
)

app = Flask(__name__)

# Initialize the database
db = SQLAlchemy(app)

# Create the database tables
@app.before_first_request
def create_tables():
    db.create_all()


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



# delay CONSTANT
DELAY = 2

# Initialize Amadeus API client with credentials from environment variables


# Helper function to fetch flight offers for a specific airport
def fetch_flight_offers_for_airport(airport, origin, date, max_price, max_retries=3):
    delay = DELAY  # Start with a 2-second delay
    for attempt in range(max_retries):
        try:
            # Make a request to the Amadeus API to get flight offers
            response = amadeus.shopping.flight_offers_search.get(
                originLocationCode=origin,
                destinationLocationCode=airport["iataCode"],
                departureDate=date,
                maxPrice=int(max_price),
                adults=1
            )
            return response
        except Exception as e:
            # Handle rate limiting by retrying with exponential backoff
            if "[429]" in str(e):
                print(f"Received 429 for airport {airport['iataCode']}, retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2  # Optionally use exponential backoff: 2, 4, 8 seconds, etc.
            else:
                # Print any other errors and return None
                print(f"Error fetching flights for airport {airport['iataCode']}: {e}")
                return None
    # Print a message if all retries fail
    print(f"Failed fetching flights for airport {airport['iataCode']} after retries.")
    return None

# Function to get airport suggestions based on a query
def get_airport_suggestions(query):
    """Fetches airport suggestions from Amadeus API."""
    try:
        # Ensure the query is at least 3 characters long to prevent invalid API requests
        if len(query) < 3:
            return []

        # Make a request to the Amadeus API to get airport suggestions based on the query
        response = amadeus.reference_data.locations.get(
            keyword=query,
            subType="AIRPORT"
        )
        print("Airport API Response:", response.data)  # Debugging

        # Extract and return relevant information from the API response
        return [{"name": loc["name"], "code": loc["iataCode"]} for loc in response.data]
    except Exception as e:
        # Handle any exceptions that occur during the API request
        print("Error fetching airports:", e)
        return []

# Function to get flight deals based on origin, date, max price, and destination country
def get_flight_deals(origin, date, max_price, country_dest):
    """Fetches the cheapest flight deals from Amadeus API."""
    try:
        # Validate the origin IATA code
        if not origin or len(origin) != 3:
            print("Invalid IATA code:", origin)
            return []

        # Set a default maximum price if none is provided
        max_price = int(max_price) if max_price and str(max_price).isdigit() else 500

        # Retrieves all airports in specified destination country
        airports = get_airports(country_dest)

        if len(airports) == 0:
            print("No airports were found for country:", country_dest)
            return []

        results = []
        # Use a thread pool to fire off API calls concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            future_to_airport = {
                executor.submit(
                    amadeus.shopping.flight_offers_search.get,
                    originLocationCode=origin,
                    destinationLocationCode=airport["iataCode"],
                    departureDate=date,
                    maxPrice=int(max_price),
                    adults=1
                ): airport for airport in airports
            }
            for future in concurrent.futures.as_completed(future_to_airport):
                try:
                    # Collect the response from each future
                    response = future.result()
                    results.append(response)
                except Exception as e:
                    # Print any errors that occur during the API request
                    print("Error fetching flights for an airport:", e)
                    continue

        # Process all responses and build the flight deals list
        flight_deals = [
            {
                "departure": offer["itineraries"][0]["segments"][0]["departure"]["iataCode"],
                "destination": offer["itineraries"][0]["segments"][-1]["arrival"]["iataCode"],
                "departure_date": offer["itineraries"][0]["segments"][0]["departure"]["at"],
                "price": offer["price"]["total"],
                # Use an internal route for booking (see next section)
                "link": offer.get("bookingUrl")
            }
            for response in results
            for offer in response.data
        ]
        return flight_deals
    except Exception as e:
        import traceback
        # Print any outer errors that occur during the process
        print("Outer Err fetching flights:", e)
        traceback.print_exc()
        return []

# Function to get a list of airports for a given country keyword
def get_airports(country):
    """Fetches a list of airports for a given country keyword."""
    try:
        # Make a request to the Amadeus API to get airports based on the country keyword
        response = amadeus.reference_data.locations.get(
            keyword=country,  # Using the country code directly
            subType="AIRPORT"
        )

        # Extract and return relevant information from the API response
        airports = [
            {
                "name": location["name"],
                "iataCode": location["iataCode"],
                "city": location["address"]["cityName"],
                "country": location["address"]["countryCode"]
            }
            for location in response.data
        ]
        # Remove filtering to return all airports found
        return airports
    except ResponseError as error:
        # Print any errors that occur during the API request
        print("Error fetching airports:", error)
        return []


# Route to get airport suggestions based on a query
@app.route("/get_airports", methods=["GET"])
def get_airports():
    # Get the query parameter 'q' from the request
    query = request.args.get("q", "")
    # Fetch airport suggestions using the query
    airports = get_airport_suggestions(query)
    # Return the suggestions as a JSON response
    return jsonify(airports)

# Route to search for flight deals
@app.route("/search_flights", methods=["POST"])
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




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)