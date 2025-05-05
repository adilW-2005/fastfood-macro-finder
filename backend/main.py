from flask import Flask, request, jsonify
from flask_cors import CORS
import googlemaps
from nutrition import search_restauraunt
from ai import nlp_to_json
from config import app
from data import data_bp  # Import the Blueprint from data.py
from auth import auth_bp

CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:5173"}})

app.register_blueprint(data_bp)
app.register_blueprint(auth_bp, url_prefix="/auth")



API_KEY = "AIzaSyD1pyG_f8vKO_NHtUkMJwkbFq4Pg1vecUs"
N_API_KEY = "YOUR_NUTRITION_API_KEY"

@app.route("/recommendations", methods=['POST'])
def get_recommendation():

    data = request.get_json()

    if not data or "location" not in data:
        return jsonify({"error": "Location is required"}), 400
    
    if "nlp_query" in data and data["nlp_query"].strip():
        nlp_data = nlp_to_json(data["nlp_query"])
        if nlp_data:
            for key, value in nlp_data.items():
                if not data.get(key):  
                    data[key] = value 


    location = data["location"]
    max_calories = float(data.get("max_calories", 0))
    min_protein = float(data.get("min_protein", 0))
    radius_search = int(data.get("radius_search", 1000)) 
    sort_by = data.get("sort_by", None)
    gmaps = googlemaps.Client(key=API_KEY)
    geocode_result = gmaps.geocode(location)

    geo_location = geocode_result[0]['geometry']['location']
    latitude, longitude = geo_location['lat'], geo_location['lng']
    formatted_address = geocode_result[0]['formatted_address']

    places_result = gmaps.places_nearby(location=(latitude, longitude), radius=radius_search, open_now=False, type="restaurant")

    restaurant_names = [place["name"] for place in places_result["results"]]

    restaurants_data = []  # ✅ List to store restaurant details

    for place in places_result["results"]:
        restaurant_info = {
            "name": place.get("name"),
            "address": place.get("vicinity"),
            "latitude": place["geometry"]["location"]["lat"],
            "longitude": place["geometry"]["location"]["lng"],
        }
        restaurants_data.append(restaurant_info)

    menu_items = []
    for restaurant in restaurant_names:
        menu_data = search_restauraunt(restaurant, max_calories=max_calories, min_protein=min_protein, sort_by=None)
        for item in menu_data.values():
            item["restaurant_name"] = restaurant
            menu_items.append(item)

    if sort_by:
        if sort_by == "calories":
            menu_items.sort(key=lambda x: x["calories"])
        elif sort_by == "protein":
            menu_items.sort(key=lambda x: x["protein"], reverse=True)

    return jsonify({
        "message": "Recommendations generated successfully!",
        "location": formatted_address,
        "restaurants": menu_items,
        "brand_names": restaurants_data,
        "user_latitude":latitude,
        "user_longitude" : longitude,
        "max_calories": max_calories,
        "min_protein": min_protein,
        "radius_search": radius_search
    }), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
