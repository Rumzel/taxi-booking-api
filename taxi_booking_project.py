# Taxi Booking Project using Python and APIs

from flask import Flask, request, jsonify
import requests
from shapely.geometry import Point, Polygon
from geopy.distance import geodesic
import json

app = Flask(__name__)

# Global API key
GOOGLE_API_KEY = "AIzaSyDJDp22V5_pgWzvDE-mh2N76bWciNL3BIA"  # Replace with your actual Google API key

def google_autocomplete(api_key, address):
    """Fetch suggestions for an address using Google Places API."""
    url = f"https://maps.googleapis.com/maps/api/place/autocomplete/json"
    params = {
        'input': address,
        'key': api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()['predictions']
    else:
        return []

def google_directions(api_key, origin, destination):
    """Fetch directions between origin and destination using Google Directions API."""
    url = f"https://maps.googleapis.com/maps/api/directions/json"
    params = {
        'origin': origin,
        'destination': destination,
        'key': api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        directions = response.json()
        if directions['routes']:
            polyline = directions['routes'][0]['overview_polyline']['points']
            return {
                'polyline': polyline
            }
        else:
            return None
    else:
        return None

def get_city_polygon(city_name):
    """Fetch the polygon of a city using Nominatim API."""
    url = "https://nominatim.openstreetmap.org/search.php"
    params = {
        'q': city_name,
        'polygon_geojson': 1,
        'format': 'json'
    }
    headers = {
        'User-Agent': 'TaxiBookingApp/1.0 (your_email@example.com)'  # Укажите свой email для идентификации
    }
    response = requests.get(url, params=params, headers=headers)
    #print(f"API Response Status: {response.status_code}")
    #print(f"API Response Content: {response.text}")
    if response.status_code == 200:
        data = response.json()
        if data and 'geojson' in data[0]:
            coordinates = data[0]['geojson']['coordinates'][0]
            return [{'lon': coord[0], 'lat': coord[1]} for coord in coordinates]
    return None

def decode_polyline(polyline_str):
    """Decode a polyline into a list of latitude and longitude points."""
    import polyline
    return polyline.decode(polyline_str)

def calculate_city_and_outside_distance(points, city_polygon):
    """Calculate distances within and outside the city."""
    city_polygon = Polygon([(p['lon'], p['lat']) for p in city_polygon])
    city_distance = 0
    outside_distance = 0

    for i in range(len(points) - 1):
        point1 = Point(points[i][1], points[i][0])
        point2 = Point(points[i + 1][1], points[i + 1][0])

        segment_distance = geodesic((points[i][0], points[i][1]), (points[i + 1][0], points[i + 1][1])).km

        if city_polygon.contains(point1) and city_polygon.contains(point2):
            city_distance += segment_distance
        else:
            outside_distance += segment_distance

    return city_distance, outside_distance

def calculate_cost(city_distance, outside_distance, city_rate=10, outside_rate=15, base=40):
    """Calculate fare based on city and outside distances."""
    city_fare = city_distance * city_rate
    outside_fare = outside_distance * outside_rate
    return base + city_fare + outside_fare

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    address = request.args.get('address')
    if not address:
        return jsonify({"error": "Address parameter is required"}), 400
    suggestions = google_autocomplete(GOOGLE_API_KEY, address)
    return jsonify(suggestions)

@app.route('/calculate', methods=['GET'])
def calculate():
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    if not origin or not destination:
        return jsonify({"error": "Both origin and destination parameters are required"}), 400
    
    route_info = google_directions(GOOGLE_API_KEY, origin, destination)
    if not route_info:
        return jsonify({"error": "Could not calculate the route"}), 400

    polyline_points = decode_polyline(route_info['polyline'])

    city_name = request.args.get('city', 'Kyiv')
    city_polygon = get_city_polygon(city_name)
    if not city_polygon:
        return jsonify({"error": f"City polygon for {city_name} not found"}), 400

    city_distance, outside_distance = calculate_city_and_outside_distance(polyline_points, city_polygon)
    cost = calculate_cost(city_distance, outside_distance)

    return jsonify({
        "origin": origin,
        "destination": destination,
        "city_distance_km": city_distance,
        "outside_distance_km": outside_distance,
        "total_distance_km": city_distance + outside_distance,
        "cost": cost
    })

if __name__ == "__main__":
    app.run(debug=True)
