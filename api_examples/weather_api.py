"""
Open-Meteo Weather API - GET Request with Parameters
-----------------------------------------------------
Fetches current weather and forecast data
No API key required!
"""

import requests
import json
from datetime import datetime

print("=" * 60)
print("WEATHER API - OPEN-METEO")
print("=" * 60)
print()

def get_weather_open_meteo(lat, lon, city_name="Unknown"):
    """
    Fetch current + hourly forecast weather data from Open-Meteo
    for the given latitude and longitude.
    """
    base_url = "https://api.open-meteo.com/v1/forecast"
    
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "hourly": "temperature_2m,precipitation_probability,windspeed_10m",
        "forecast_days": 1
    }
    
    print(f"Fetching weather for: {city_name}")
    print(f"Coordinates: {lat}, {lon}")
    print()
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return None
    
    return response.json()

def pretty_print(data, city_name):
    if not data:
        return
    
    print("=" * 60)
    print(f"CURRENT WEATHER - {city_name.upper()}")
    print("=" * 60)
    
    # Current weather
    cw = data.get("current_weather", {})
    print(f"Temperature: {cw.get('temperature')}°C")
    print(f"Wind Speed: {cw.get('windspeed')} km/h")
    print(f"Wind Direction: {cw.get('winddirection')}°")
    print(f"Weather Code: {cw.get('weathercode')}")
    print(f"Time: {cw.get('time')}")
    print()
    
    # Hourly forecast (first 6 hours)
    print("=" * 60)
    print("HOURLY FORECAST (Next 6 Hours)")
    print("=" * 60)
    hourly = data.get("hourly", {})
    times = hourly.get("time", [])[:6]
    temps = hourly.get("temperature_2m", [])[:6]
    rain = hourly.get("precipitation_probability", [])[:6]
    wind = hourly.get("windspeed_10m", [])[:6]
    
    for i in range(len(times)):
        print(f"{times[i]} | Temp: {temps[i]}°C | Rain: {rain[i]}% | Wind: {wind[i]} km/h")
    print()

# Example cities
cities = [
    {"name": "New Delhi", "lat": 28.6139, "lon": 77.2090},
    {"name": "Mumbai", "lat": 19.0760, "lon": 72.8777},
    {"name": "Bangalore", "lat": 12.9716, "lon": 77.5946},
]

# Collect weather data for all cities
all_weather_data = []

for city in cities:
    data = get_weather_open_meteo(city["lat"], city["lon"], city["name"])
    if data:
        pretty_print(data, city["name"])
        all_weather_data.append({
            "city": city["name"],
            "data": data,
            "fetched_at": datetime.now().isoformat()
        })

# Save all data
output_file = "datasets/weather_data.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_weather_data, f, indent=4)

print("=" * 60)
print(f"✅ Weather data saved to: {output_file}")
print("=" * 60)
