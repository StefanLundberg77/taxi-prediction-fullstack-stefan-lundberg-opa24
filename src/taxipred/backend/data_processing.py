from taxipred.utils.constants import get_clean_data, get_taxi_model
from pydantic import BaseModel, Field
import pandas as pd
import json
from pprint import pprint
from dotenv import load_dotenv
import os
import requests

# load .env file
load_dotenv() 


class TaxiInput(BaseModel):
    Trip_Distance_km: float = Field(ge=1, le=10000)
    Base_Fare: float = Field(ge=1, le=10)
    Per_Km_Rate: float = Field(ge=0, le=10)
    Per_Minute_Rate: float = Field(ge=0, le=10)
    Trip_Duration_Minutes: float = Field(ge=0, le=10000)
    Day_of_Week_Weekday: bool
    Traffic_Conditions_High: bool
    Weather_Rain: bool
    Weather_Snow: bool
    Day_of_Week_Weekday: bool
    Passenger_Count: float = Field(ge=0, le=9)
    Time_of_Day_Afternoon: bool
    Traffic_Conditions_High: bool

class PredictionOutput(BaseModel):
    predicted_trip_price: float = Field(ge=0.1, description="Predicted price in SEK.")

    
class TaxiData:
    def __init__(self):
        self.df = get_clean_data()
        self.model = get_taxi_model()
        self.conversion_rate = self.fetch_currency_rate()

    def to_json(self):
        return json.loads(self.df.to_json(orient = "records"))
    
    # method: fetch current currency rate from api
    def fetch_currency_rate(default_rate: float = 10.0) -> float:
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
    
    # trip price prediction method
    def predict(self, input_data: TaxiInput) -> PredictionOutput:

        # Convert input to DataFrame
        input = input_data#
        input_df = pd.DataFrame([input]) #input type?

        # Remove  
        if "Trip_Price" in input_df.columns:
            input_df = input_df.drop(columns=["Trip_Price"])
        
        # Prediction
        price_prediction = self.model.predict(input_df)[0]
        sek_price = round(float(price_prediction) * self.conversion_rate, 2)

        return PredictionOutput(predicted_trip_price=sek_price)







if __name__ == "__main__":
    taxi_data = TaxiData()
    #pprint(taxi_data.to_json())
    
    payload = {
        "Trip_Distance_km": 12,
        "Passenger_Count" : 2,
        "Base_Fare": 2,
        "Per_Km_Rate": 2,
        "Per_Minute_Rate": 0.5,
        "Trip_Duration_Minutes": 32, 
        "Time_of_Day_Afternoon": True,
        "Day_of_Week_Weekday": False,
        "Traffic_Conditions_High": False,
        "Weather_Rain": True,
        "Weather_Snow": False,
    }
    
    pprint(taxi_data.predict(payload))


#  #   Column                   Non-Null Count  Dtype  
# ---  ------                   --------------  -----  
#  0   Trip_Distance_km         1000 non-null   float64
#  1   Passenger_Count          1000 non-null   float64
#  2   Base_Fare                1000 non-null   float64
#  3   Per_Km_Rate              1000 non-null   float64
#  4   Per_Minute_Rate          1000 non-null   float64
#  5   Trip_Duration_Minutes    1000 non-null   float64
#  6   Time_of_Day_Afternoon    1000 non-null   bool   
#  7   Day_of_Week_Weekday      1000 non-null   bool   
#  8   Traffic_Conditions_High  1000 non-null   bool   
#  9   Weather_Rain             1000 non-null   bool   
#  10  Weather_Snow             1000 non-null   bool   
#  11  Trip_Price               1000 non-null   float64
    
# Index(['Trip_Distance_km', 'Base_Fare', 'Per_Km_Rate', 'Per_Minute_Rate',
#        'Trip_Duration_Minutes', 'Time_of_Day_Afternoon', 'Day_of_Week_Weekday',
#        'Traffic_Conditions_High', 'Weather_Rain', 'Weather_Snow',
#        'Trip_Price'],
#       dtype='object')

# drop(["Time_of_Day_Night",
# "Time_of_Day_Evening",
# "Time_of_Day_Morning",
# "Day_of_Week_Weekend",
# "Traffic_Conditions_Low",
# "Weather_Clear",
# "Traffic_Conditions_Medium"],
# axis="columns"
# )"

# count	mean	std	min	25%	50%	75%	max
# Trip_Distance_km	1000.0	26.153327	15.521566	1.23	13.1075	26.995000	37.7825	74.795
# Base_Fare	1000.0	3.502989	0.848107	2.01	2.7700	3.502989	4.2025	5.000
# Per_Km_Rate	1000.0	1.233316	0.418922	0.50	0.8700	1.233316	1.5800	2.000
# Per_Minute_Rate	1000.0	0.292916	0.112662	0.10	0.1975	0.292916	0.3825	0.500
# Trip_Duration_Minutes	1000.0	62.118116	31.339413	5.01	37.1075	62.118116	87.7750	119.840