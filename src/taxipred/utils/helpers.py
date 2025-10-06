import requests 
from urllib.parse import urljoin
from pprint import pprint
from datetime import datetime
from dotenv import load_dotenv
import os

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
def get_currency_rate(self, default_rate: float = 10.0) -> float:
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

        


# TODO: 
#- finish distance_duration
#- weather api?
#- traffic condition api?
#- map