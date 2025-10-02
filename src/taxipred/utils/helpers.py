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
    pprint(read_api_endpoint("/api").json())

    payload = {
        "Trip_Distance_km": 12,
        "Base_Fare": 2,
        "Per_Km_Rate": 2,
        "Per_Minute_Rate": 0.5,
        "Trip_Duration_Minutes": 32,
        # "Time_of_Day_Afternoon: 
        # "Day_of_Week_Weekday": 
        # "Traffic_Conditions_High": 
        # "Weather_Rain": 
        # "Weather_Snow": 
        # "Trip_Price":
    }
    pprint(post_api_endpoint(payload=payload, endpoint="/api/predict").json())


# TODO:
# post_api_endpoint
        
        
        # "SepalLengthCm": 6,
        # "SepalWidthCm": 3,
        # "PetalLengthCm": 3.8,
        # "PetalWidthCm": 1.2,
        
        #               count	mean	    std	        min	    25%	    50%	        75%	    max
# Trip_Distance_km	    1000.0	26.153327	15.521566	1.23	13.1075	26.995000	37.7825	74.795
# Base_Fare	            1000.0	3.502989	0.848107	2.01	2.7700	3.502989	4.2025	5.000
# Per_Km_Rate	        1000.0	1.233316	0.418922	0.50	0.8700	1.233316	1.5800	2.000
# Per_Minute_Rate	    1000.0	0.292916	0.112662	0.10	0.1975	0.292916	0.3825	0.500
# Trip_Duration_Minutes	1000.0	62.118116	31.339413	5.01	37.1075	62.118116	87.7750	119.840