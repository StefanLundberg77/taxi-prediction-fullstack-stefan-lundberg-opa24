from taxipred.utils.constants import get_clean_data, get_taxi_model
from pydantic import BaseModel, Field
import pandas as pd
import json
from pprint import pprint

class TaxiInput(BaseModel):
    Trip_Distance_km: float = Field(ge=1, le=10000)
    Base_Fare: float = Field(ge=1, le=10)
    Per_Km_Rate: float = Field(ge=0, le=10)
    Per_Minute_Rate: float = Field(ge=0, le=10)
    Trip_Duration_Minutes: float = Field(ge=0, le=10000)
    Time_of_Day_Afternoon: str
    Day_of_Week_Weekday: str
    Traffic_Conditions_High: str
    Weather_Rain: str
    Weather_Snow: str
    Trip_Price: float    # refactor to SEK


class PredictionOutput(BaseModel):
    predicted_trip_price: float = Field(..., description="Predicted price")

class TaxiData:
    def __init__(self):
        self.df = get_clean_data()
        self.model = get_taxi_model()

    def to_json(self):
        return json.loads(self.df.to_json(orient = "records"))
    
    




if __name__ == "__main__":
    taxi_data = TaxiData()
    pprint(taxi_data.to_json())

    
    
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