import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

lat = 13.0
lon = 80.0 #chennai for testing and viewing all data parameters

params = {
        "lat": lat,
        "lon": lon,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

response = requests.get(BASE_URL, params=params, timeout=5)
response.raise_for_status()

data = response.json()

print(data)
