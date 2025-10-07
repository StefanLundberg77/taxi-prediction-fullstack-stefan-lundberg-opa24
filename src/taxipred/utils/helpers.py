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
import time
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
    #departure_time = int(time.time())
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
        return {} # or None...
    
    # response = requests.get(url, parameters)
    # data = response.json()
    
    # try:
    #     element = data["rows"][0]["elements"][0]
    #     distance_km = element["distance"]["value"] / 1000  # meters to km
    #     duration_min = element["duration"]["value"] / 60   # seconds to minutes
    #     return distance_km, duration_min
    # except Exception as e:
    #     print("Error:", e)
    #     return None, None

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
      style="border:0"
      loading="lazy"
      allowfullscreen
      src="https://www.google.com/maps/embed/v1/directions?key={api_key}&origin={origin_q}&destination={dest_q}&mode=driving">
    </iframe>
    """
    st.components.v1.html(iframe, height=530)
    
"""
def display_map(origin_address=None, destination_address=None):
    geolocator = Nominatim(user_agent="TAXIFY", timeout=5)
    origin = origin_address or "malmö"
    destination = destination_address or "malmö"
    
    #default_address = "Malmö, Sweden"
    # Use default if no address is provided
    #input_address = address if address else default_address
        
    origin_location = geolocator.geocode(origin)
    destination_location = geolocator.geocode(destination)
    
    # making sure location is geocode and not None to avoid AttributeError 
    if origin_location and destination_location:# is not None
        #origin_coords = [hasattr(origin_location, "latitude"), hasattr(origin_location, "longitude")] 
        #destination_coords = [hasattr(destination_location, "latitude"), hasattr(destination_location, "longitude")] 

        origin_coords = [origin_location.latitude, origin_location.longitude]
        destination_coords = [destination_location.latitude, destination_location.longitude]
        
        m= folium.Map(location=origin_coords, zoom_start=10)

        # lat, lon = location.latitude, location.longitude
        # add markers
        folium.Marker(origin_coords, tooltip=f"Start: {origin}").add_to(m)
        folium.Marker(destination_coords, tooltip=f"Destination: {destination}").add_to(m)
        
        # add line between markers
        folium.PolyLine([origin_coords, destination_coords], color="blue", weight=3).add_to(m)
        
        st_folium(m,width="stretch", height=530)
    else:
        st.error("Could not geocode input addresses")
"""
    
# TODO: 
#- finish distance_duration
#- weather api?
#- traffic condition api?
#- map /done
#- error, exception handling