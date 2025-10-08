from importlib.resources import files
import pandas as pd
import joblib

## define file paths using importlib to ensure compatibility across environments
TAXI_CSV_PATH = files("taxipred").joinpath("data/taxi_trip_pricing.csv") # Raw taxi trip data

CLEAN_CSV_PATH = files("taxipred").joinpath("data/cleaned_data.csv") # Preprocessed dataset used for training

TAXI_MODEL_PATH = files("taxipred").joinpath("models/xgb_model.joblib") # Trained XGBoost mode

MISSING_LABEL_PATH = files("taxipred").joinpath("data/missing_label.json") # Input rows with missing price labels

ASSETS_PATH = files("taxipred").joinpath("assets/") # Path to static assets ex. images

# load raw taxi trip data from CSV
def get_taxi_data():
    return pd.read_csv(TAXI_CSV_PATH)

# load cleaned dataset used for training or prediction
def get_clean_data():
    return pd.read_csv(CLEAN_CSV_PATH)

# Load trained model from disk
def get_taxi_model():
    return joblib.load(TAXI_MODEL_PATH)

# Load input rows with missing labels for testing predictions
def get_missing_label():
    return pd.read_json(MISSING_LABEL_PATH)
