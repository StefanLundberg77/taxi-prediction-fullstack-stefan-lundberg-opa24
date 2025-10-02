from fastapi import FastAPI
from taxipred.backend.data_processing import TaxiData, TaxiInput, PredictionOutput
from taxipred.utils.constants import get_taxi_model
import pandas as pd

app = FastAPI()
taxi_data = TaxiData()

@app.get("/api/")
async def read_taxi_data():
    return taxi_data.to_json()

@app.post("/api/predict", response_model=PredictionOutput)
def predict_price(payload: TaxiInput):
    data_to_predict = pd.DataFrame([payload.model_dump()])
    clf = get_taxi_model()
    prediction = clf.predict(data_to_predict)
    return {"predicted_price": prediction[0]}
    






# @app.post("/api/predict", response_model=PredictionOutput)
# def predict_flower(payload: IrisInput):
#     data_to_predict = pd.DataFrame([payload.model_dump()])
#     clf = joblib.load(MODELS_PATH / "iris_classifier.joblib")
#     prediction = clf.predict(data_to_predict)
#     return {"predicted_flower": prediction[0]}