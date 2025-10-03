import requests 
from urllib.parse import urljoin
from pprint import pprint


def read_api_endpoint(endpoint = "/", base_url = "http://127.0.0.1:8000"):
    url = urljoin(base_url, endpoint) # adds the str endpoint and a endpoint "/" if missing
    response = requests.get(url) # returns a response object
    
    return response

def post_api_endpoint(payload, endpoint = "/", base_url = "http://127.0.0.1:8000"):
    url = urljoin(base_url, endpoint)
    response = requests.post(url=url, json=payload)
    
    return response

if __name__ == '__main__':
    
    payload = {
    "Trip_Distance_km": 12,
    "Passenger_Count": 2,
    "Base_Fare": 2,
    "Per_Km_Rate": 2,
    "Per_Minute_Rate": 0.5,
    "Trip_Duration_Minutes": 32,
    "Time_of_Day_Afternoon": True,
    "Day_of_Week_Weekday": False,
    "Traffic_Conditions_High": False,
    "Weather_Rain": True,
    "Weather_Snow": False
    }

# response = post_api_endpoint(payload, endpoint="/api/predict")
# pprint(response.json())