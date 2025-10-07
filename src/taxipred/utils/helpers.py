import requests 
from urllib.parse import urljoin
from pprint import pprint
from datetime import datetime
from dotenv import load_dotenv
import os
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import streamlit as st

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
def get_distance_duration(origin, destination):
    api_key = os.getenv("GOOGLE_MAPS_KEY")
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    parameters = {
        "origins": origin,
        "destinations": destination,
        "units": "metric",
        "key": api_key            
    }
    response = requests.get(url, parameters)
    data = response.json()
    
    try:
        element = data["rows"][0]["elements"][0]
        distance_km = element["distance"]["value"] / 1000  # meters to km
        duration_min = element["duration"]["value"] / 60   # seconds to minutes
        return distance_km, duration_min
    except Exception as e:
        print("Error:", e)
        return None, None

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

def display_map(address):
    geolocator = Nominatim(user_agent="TAXIFY")
    default_address = "Uppsala, Sweden"
    
    if not address:
        address = default_address
        location = address
        m= folium.Map(location=[location.latitude, location.longitude], zoom_start=10)
        folium.Marker([location.latitude, location.longitude], tooltip=location).add_to(m)
        st_folium(m, width=800, height=200)
        
    location = geolocator.geocode(address)
    
    if location:
        m= folium.Map(location=[location.latitude, location.longitude], zoom_start=10)
        folium.Marker([location.latitude, location.longitude], tooltip=location).add_to(m)
        st_folium(m, width=800, height=200)
    else:
        # if geocode fail, display deafault
        fallback_location = geolocator.geocode(default_address)
        if fallback_location:
            m= folium.Map(location=[fallback_location.latitude, fallback_location.longitude], zoom_start=10)
            folium.Marker([fallback_location.latitude, fallback_location.longitude], tooltip=location).add_to(m)
            st_folium(m, width=800, height=200)
            
        else:
            st.error("No address")
# TODO: 
#- finish distance_duration
#- weather api?
#- traffic condition api?
#- map
#- error, exception handling