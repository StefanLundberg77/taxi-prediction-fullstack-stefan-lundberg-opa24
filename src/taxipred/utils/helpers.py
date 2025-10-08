import requests 
from urllib.parse import urljoin
from dotenv import load_dotenv
import os
import streamlit as st
import urllib.parse

load_dotenv() 

def read_api_endpoint(endpoint = "/", base_url = "http://127.0.0.1:8000"):
    url = urljoin(base_url, endpoint) # adds the str endpoint and a endpoint "/" if missing
    response = requests.get(url) # returns a response object
    
    return response

def post_api_endpoint(payload, endpoint = "/", base_url = "http://127.0.0.1:8000"):
    url = urljoin(base_url, endpoint)
    response = requests.post(url=url, json=payload)
    
    return response

# method: fetch current currency rate from api
def get_currency_rate(default_rate: float = 10.0) -> float:
    api_key = os.getenv("FASTFOREX_API_KEY")

    # incase api key missing use set rate
    if not api_key:
        print(f"API-key not found. Using fallback rate ({default_rate} USD/SEK).")
        return default_rate
    
    url = "https://api.fastforex.io/fetch-one"
    params = {"from": "USD", "to": "SEK"}
    headers = {"X-API-Key": api_key}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=5) # timeout incase slow responce 
        response.raise_for_status()
        data = response.json()
        return float(data["result"]["SEK"])
    except Exception as e:
        print(f" Unable to fetch currency rate from API: {e}. Using fallback rate ({default_rate} USD/SEK).")
        return default_rate

    
# input 2 adresses and get distance and estimated trip duration from google maps
def get_trip_metrics(origin, destination, departure_timestamp):
    api_key = os.getenv("GOOGLE_MAPS_KEY")
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"

    parameters = {
        "origins": origin,
        "destinations": destination,
        "units": "metric",
        "departure_time": departure_timestamp,
        "key": api_key            
    }
    try:
        response = requests.get(url, params=parameters)
        data = response.json()
        element = data["rows"][0]["elements"][0]

        distance_km = element["distance"]["value"] / 1000
        duration_min = element["duration"]["value"] / 60
        duration_traffic_min = element.get("duration_in_traffic", {}).get("value", element["duration"]["value"]) / 60

        traffic_ratio = duration_traffic_min / duration_min
        traffic_high = traffic_ratio > 1.25  # adjustable

        return distance_km, duration_min, traffic_high
    
    except Exception as e:
        print("Trip metrics error:", e)
        return None, None, False
    

def get_coordinates(address):
    api_key = os.getenv("GOOGLE_MAPS_KEY")
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": api_key
    }
        
    response = requests.get(url, params=params)
    data = response.json()
    try:
        location = data["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]
    except Exception as e:
        print("geocode error:", e)
        return None, None

def get_map_directions(origin: str, destination: str):
    
    api_key = os.getenv("GOOGLE_MAPS_KEY")
    origin_q = urllib.parse.quote(origin)
    dest_q = urllib.parse.quote(destination)

    iframe = f"""
    <iframe
      width="100%"
      height="500"
      style="border:1"
      loading="lazy"
      allowfullscreen
      src="https://www.google.com/maps/embed/v1/directions?key={api_key}&origin={origin_q}&destination={dest_q}&mode=driving">
    </iframe>
    """
    st.components.v1.html(iframe, height=500)


def get_weather(lat,lon):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        weather = data["weather"][0]["main"]

        rain = "Rain" in weather
        snow = "Snow" in weather
        return rain, snow
    except Exception as e:
        print("OpenWeather error:", e)
        return False, False

    
    
# TODO: 
#- finish distance_duration /done
#- weather api?
#- traffic condition api? /done
#- map /done
#- error, exception handling