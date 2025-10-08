from taxipred.utils.constants import get_clean_data, get_taxi_model
from pydantic import BaseModel, Field
import pandas as pd
import json
from pprint import pprint
from dotenv import load_dotenv
from taxipred.utils.helpers import get_currency_rate

# load .env file with api key etc.
load_dotenv() 

# input class for prediction requests
class TaxiInput(BaseModel):
    Trip_Distance_km: float = Field(ge=0, le=10000)
    Passenger_Count: float = Field(ge=0, le=9)
    Base_Fare: float = Field(ge=0, le=10)
    Per_Km_Rate: float = Field(ge=0, le=10)
    Per_Minute_Rate: float = Field(ge=0, le=10)
    Trip_Duration_Minutes: float = Field(ge=0, le=10000)
    Time_of_Day_Afternoon: bool
    Time_of_Day_Evening: bool
    Day_of_Week_Weekday: bool
    Traffic_Conditions_High: bool
    Weather_Rain: bool
    Weather_Snow: bool
    
# output class for prediction responses
class PredictionOutput(BaseModel):
    predicted_trip_price: float = Field(ge=0.1, description="Predicted price in SEK.")

# main class for handling predicts and data    
class TaxiData:
    def __init__(self):
        self.df = get_clean_data()
        self.model = get_taxi_model()
        # get currency conversion from USD to SEK
        self.conversion_rate = get_currency_rate()

    # return dataframe to json method
    def to_json(self):
        return json.loads(self.df.to_json(orient = "records"))
        
    # trip price prediction based on input features
    def predict(self, input_data: TaxiInput) -> PredictionOutput:

        # Convert input to DataFrame
        input_dict = input_data.model_dump()
        input_df = pd.DataFrame([input_dict])

        # Remove target column (y) if in input 
        if "Trip_Price" in input_df.columns:
            input_df = input_df.drop(columns=["Trip_Price"])
        
        # Run prediction model and convert currency
        price_prediction = self.model.predict(input_df)[0]
        sek_price = round(float(price_prediction) * self.conversion_rate, 2)

        return PredictionOutput(predicted_trip_price=sek_price)

# for testing: instantiation
if __name__ == "__main__":
    taxi_data = TaxiData()
    