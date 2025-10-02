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

# import requests 
# from urllib.parse import urljoin

# def read_api_endpoint(endpoint = "/", base_url = "http://127.0.0.1:8000"):
#     url = urljoin(base_url, endpoint)
#     response = requests.get(url)
    
#     return response

# TODO:
# post_api_endpoint