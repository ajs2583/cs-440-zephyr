from amadeus import Client, ResponseError
from os import getenv
import concurrent.futures
import time

# delay CONSTANT
DELAY = 2

# Initialize Amadeus API client with credentials from environment variables
amadeus = Client(
    client_id=getenv("AMADEUS_API_KEY"),
    client_secret=getenv("AMADEUS_API_SECRET")
)

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
