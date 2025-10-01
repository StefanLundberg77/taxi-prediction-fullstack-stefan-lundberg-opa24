from importlib.resources import files
import pandas as pd
import joblib

TAXI_CSV_PATH = files("taxipred").joinpath("data/taxi_trip_pricing.csv")

CLEAN_CSV_PATH = files("taxipred").joinpath("data/cleaned_data.csv")

TAXI_MODEL_PATH = files("taxipred").joinpath("models/xgb_model.joblib")

def get_taxi_data():
    return pd.read_csv(TAXI_CSV_PATH)

def get_clean_data():
    return pd.read_csv(CLEAN_CSV_PATH)

def get_taxi_model():
    return joblib.load(TAXI_MODEL_PATH)