import geopy
import os
from geopy.geocoders import Nominatim
import requests
from dotenv import load_dotenv

load_dotenv()

Weather_API_KEY = os.getenv("WEATHER_API_KEY")
if Weather_API_KEY is None:
    print("Please set the WEATHER_API_KEY environment variable.")
    exit(1)

Nominatim = Nominatim(user_agent="weather_app")

location = Nominatim.geocode(input("Enter a location: "), timeout=10)

LATT, LONN = (location.latitude, location.longitude)

response = requests.get("https://api.openweathermap.org/data/2.5/weather", params={"lat": LATT, "lon": LONN , "appid": Weather_API_KEY, "units": "metric"})

weather_data = response.json()

city = weather_data["name"]
description = weather_data["weather"][0]["description"]
temp = weather_data["main"]["temp"]
feels_like = weather_data["main"]["feels_like"]
humidity = weather_data["main"]["humidity"]
wind_speed = weather_data["wind"]["speed"]

print(location.address, "\n\n")
print("Weather Information:")
print(f"City: {city}")
print(f"Description: {description}")
print(f"Temperature: {temp}°C")
print(f"Feels Like: {feels_like}°C")
print(f"Humidity: {humidity}%")
print(f"Wind Speed: {wind_speed} m/s")