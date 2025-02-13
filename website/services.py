from amadeus import Client
from os import getenv

# Initialize Amadeus API client with credentials from environment variables
amadeus = Client(
    client_id=getenv("AMADEUS_API_KEY"),
    client_secret=getenv("AMADEUS_API_SECRET")
)

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
        print("Airport API Response:", response.data)                          #! Debugging

        # Extract and return relevant information from the API response
        return [{"name": loc["name"], "code": loc["iataCode"]} for loc in response.data]
    except Exception as e:
        # Handle any exceptions that occur during the API request
        print("Error fetching airports:", e)
        return []

def get_flight_deals(origin, date, max_price):
    """Fetches the cheapest flight deals from Amadeus API."""
    try:
        # Validate the origin IATA code
        if not origin or len(origin) != 3:
            print("Invalid IATA code:", origin)
            return []

        # Set a default maximum price if none is provided
        if not max_price:
            max_price = 500  # Default fallback value

        # Make a request to the Amadeus API to get flight deals
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origin,
            departureDate=date,
            maxPrice=int(max_price),  # Ensure integer type
            adults=1
        )

        print("Full Flight API Response:", response.result)                     #! Debugging

        #! Check for errors in the API response
        if "errors" in response.result:
            print("Amadeus API Error:", response.result["errors"])
            return []

        # Extract and return relevant information from the API response
        return [
            {
                "departure": offer["itineraries"][0]["segments"][0]["departure"]["iataCode"],
                "destination": offer["itineraries"][0]["segments"][-1]["arrival"]["iataCode"],
                "departure_date": offer["itineraries"][0]["segments"][0]["departure"]["at"],
                "price": offer["price"]["total"],
                "link": f"https://www.amadeus.com/book/{offer['id']}"
            }
            for offer in response.data
        ]
    except Exception as e:
        # Handle any exceptions that occur during the API request
        print("Error fetching flights:", e)
        return []
'''
 TODO This code is returning 400 (unaccepted request) but still is parsing airport data, maybe bad request/bad parameters?
'''