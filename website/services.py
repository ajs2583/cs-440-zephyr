from amadeus import Client, ResponseError
from os import getenv, path

AMADEUS_API_KEY = getenv("AMADEUS_API_KEY")
AMADEUS_API_SECRET = getenv("AMADEUS_API_SECRET")

amadeus = Client(
    client_id=AMADEUS_API_KEY,
    client_secret=AMADEUS_API_SECRET
)

def get_flight_deals(origin):
    """Fetches the cheapest flight deals from Amadeus SDK."""
    try:
        response = amadeus.shopping.flight_destinations.get(origin=origin)
        return response.data
    except Exception as e:
        return {"error": str(e)}
    