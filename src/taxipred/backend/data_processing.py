from taxipred.utils.constants import get_clean_data
from pydantic import BaseModel, Field
import pandas as pd
import json
from pprint import pprint


class TaxiData:
    def __init__(self):
        self.df = get_clean_data()

    def to_json(self):
        return json.loads(self.df.to_json(orient = "records"))

class TaxiInput(BaseModel):
    Price: float
    
class PredictionOutput():
    predicted_price: float
    
if __name__ == "__main__":
    taxi_data = TaxiData()
    pprint(taxi_data.to_json())