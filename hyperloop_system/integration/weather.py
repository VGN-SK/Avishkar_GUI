import os
import requests
import time
from typing import Dict, List
from tracking.default_tracks import get_track

from dotenv import load_dotenv

# Load environment variables from .env file -- here the api key
load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Simple in-memory cache -- so that you dont have to call weather api unnecessarily .. free plan has only limited calls per day
_weather_cache = {}
CACHE_DURATION = 300  # seconds (5 minutes)



# FETCH WEATHER FOR ONE POINT

def fetch_weather(lat: float, lon: float) -> Dict: #Calls OpenWeatherMap API for given coordinates.

    if not OPENWEATHER_API_KEY:
        raise RuntimeError("OpenWeatherMap API key not set.")

    cache_key = f"{lat}_{lon}"

    # Check cache
    if cache_key in _weather_cache:
        cached_data, timestamp = _weather_cache[cache_key]
        if time.time() - timestamp < CACHE_DURATION:
            return cached_data

    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    response = requests.get(BASE_URL, params=params, timeout=5)
    response.raise_for_status()

    data = response.json()

    structured = {
        "temperature": data["main"]["temp"],
        "wind_speed": data["wind"]["speed"],
        "rain": "rain" in data,
        "weather_description": data["weather"][0]["description"]
    }

    _weather_cache[cache_key] = (structured, time.time())

    return structured



# GET WEATHER ALONG TRACK

def get_route_weather(track_id: str) -> Dict:  #Samples weather at multiple points along track and aggregates risk. Later weather can be made dynamic and the worst weather at any waypoint will be used to assess safety


    track = get_track(track_id)

    # Sample 3 points: start, middle, end
    sample_positions = [
        0,
        track.total_length / 2,
        track.total_length
    ]

    samples: List[Dict] = []

    for pos in sample_positions:
        lat, lon = track.get_coordinates(pos)
        weather = fetch_weather(lat, lon)
        samples.append(weather)

    avg_temp = sum(s["temperature"] for s in samples) / len(samples)
    avg_wind = sum(s["wind_speed"] for s in samples) / len(samples)
    rain_present = any(s["rain"] for s in samples)

    risk_level = "low"   # these are based only on weather ... not considering velocity

    if avg_wind > 15 or rain_present:
        risk_level = "moderate"

    if avg_wind > 25:
        risk_level = "high"

    return {
        "avg_temperature": avg_temp,
        "avg_wind_speed": avg_wind,
        "rain_detected": rain_present,
        "risk_level": risk_level,
        "samples": samples
    }

