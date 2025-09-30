from taxipred.utils.constants import TAXI_CSV_PATH, CLEAN_CSV_PATH
from pydantic import BaseModel, Field
import pandas as pd
import json


class TaxiData:
    def __init__(self):
        self.df = pd.read_csv(CLEAN_CSV_PATH)

    def to_json(self):
        return json.loads(self.df.to_json(orient = "records"))

class TaxiInput(BaseModel):
    Price: float
    
class PredictionOutput():
    predicted_price: float
    
if __name__ == "__main__":
    taxi_data = TaxiData()
    print(taxi_data.to_json())