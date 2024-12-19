
# Taxi Booking API

This project provides a simple API to simulate a taxi booking system using Google Maps APIs. It offers routes for address autocompletion, route calculation, and fare estimation.

## Features
1. **Autocomplete Address Suggestions**: Uses Google Places API to fetch address suggestions.
2. **Route Calculation**: Uses Google Directions API to calculate the route, distance, and duration between two points.
3. **Fare Calculation**: Computes the cost of the trip based on a base fare, city rate, and outside city rate.
4. **City vs. Outside City Distance**: Calculates the distance traveled within the city and outside it using OpenStreetMap's Overpass API.

## Requirements
- Python 3.x
- Flask
- `requests`, `shapely`, `geopy`, and `polyline` libraries
- Google API Key with access to Places and Directions APIs

## Setup
1. Install dependencies:
   ```bash
   pip install flask requests shapely geopy polyline
   ```
2. Replace `GOOGLE_API_KEY` in the script with your actual Google API key.

## Usage
1. Run the server:
   ```bash
   python taxi_booking_project.py
   ```
2. Access the following endpoints:

### Endpoints
1. **Autocomplete Address**
   - **Method**: `GET`
   - **URL**: `/autocomplete`
   - **Parameters**: 
     - `address`: The partial address to get suggestions for.
   - **Example**:
     ```bash
     curl --get "http://127.0.0.1:5000/autocomplete" --data-urlencode "address=Kyiv Shevchenka 1"
     ```

2. **Calculate Route and Fare**
   - **Method**: `GET`
   - **URL**: `/calculate`
   - **Parameters**:
     - `origin`: Starting point.
     - `destination`: Destination point.
     - `city`: City name (default is `Kyiv`).
   - **Example**:
     ```bash
     curl --get "http://127.0.0.1:5000/calculate" \
        --data-urlencode "origin=Shevchenka Street, 1, Kyiv, Ukraine" \
        --data-urlencode "destination=Boryspil', Kyiv Oblast, Ukraine" \
        --data-urlencode "city=Kyiv"
     ```

### Example Response
```json
{
    "city_distance_km": 22.534468658649605,
    "cost": 477.5829865654356,
    "destination": "Boryspil', Kyiv Oblast, Ukraine",
    "origin": "Shevchenka Street, 1, Kyiv, Ukraine",
    "outside_distance_km": 14.149219998595973,
    "total_distance_km": 36.683688657245575
}
```

## Notes
- Ensure the Google API key has the necessary permissions.
- Adjust the `base`, `city_rate`, and `outside_rate` in the `calculate_cost` function to match desired tariffs.
- The `city` parameter is used to fetch the city polygon for determining distances inside and outside the city.

## License
This project is for educational purposes and is licensed under the MIT License.
