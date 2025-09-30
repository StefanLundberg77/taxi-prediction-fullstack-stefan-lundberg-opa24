from fastapi import FastAPI
from taxipred.backend.data_processing import TaxiData

app = FastAPI()

taxi_data = TaxiData()

@app.get("/taxi/")
async def read_taxi_data():
    return taxi_data.to_json()




@app.post("/api/predict", response_model=PredictionOutput)
def predict_flower(payload: IrisInput):
    data_to_predict = pd.DataFrame([payload.model_dump()])
    clf = joblib.load(MODELS_PATH / "iris_classifier.joblib")
    prediction = clf.predict(data_to_predict)
    return {"predicted_flower": prediction[0]}