import googlemaps
import pprint

API_KEY = "AIzaSyB8cToMsi9GpsrqL-1_-XgXDXUh5mFMGY8"

gmaps = googlemaps.Client(key=API_KEY)

def get_nearby_restaurants(location):
    # Geocode the location to get latitude and longitude
    geocode_result = gmaps.geocode(location)
    
    if not geocode_result:
        return {"error": "Location not found"}

    # Extract latitude and longitude from the geocode result
    location_data = geocode_result[0]['geometry']['location']
    latitude = location_data['lat']
    longitude = location_data['lng']

    # Get nearby restaurants using Places API
    places_result = gmaps.places_nearby(location=(latitude, longitude), radius=500, open_now=False, type="restaurant")

    # Extract restaurant names
    restaurant_names = []
    if "results" in places_result:
        for place in places_result['results']:
            restaurant_names.append(place["name"])

    return restaurant_names

# Example usage:
if __name__ == "__main__":
    location = "Austin, Texas"  # Example location
    restaurants = get_nearby_restaurants(location)
    pprint.pprint(restaurants)
