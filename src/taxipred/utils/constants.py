from importlib.resources import files
import pandas as pd

TAXI_CSV_PATH = files("taxipred").joinpath("data/taxi_trip_pricing.csv")

CLEAN_CSV_PATH = files("taxipred").joinpath("data/cleaned_data.csv")

def get_taxi_data():
    return pd.read_csv(TAXI_CSV_PATH)

def get_clean_data():
    return pd.read_csv(CLEAN_CSV_PATH)