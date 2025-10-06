from fastapi import FastAPI
from taxipred.backend.data_processing import TaxiData, TaxiInput, PredictionOutput

app = FastAPI()
taxi_data = TaxiData()

# root page message
@app.get("/")
def root():
    return {"Taxi prediction API is runnin add endpoint/docs to url for swagger UI"}

# endpoint return data in json format and limited to 100 rows
@app.get("/api/")
async def read_taxi_data():
    return taxi_data.df.head(100).to_dict(orient="records")

# endpoint use predict method from taxi class   
@app.post("/api/predict", response_model=PredictionOutput)
def predict_price(payload: TaxiInput):
    return taxi_data.predict(payload)





# TODO: 
    # - start and shutdown handling?


# @app.post("/api/predict", response_model=PredictionOutput)
# def predict_flower(payload: IrisInput):
#     data_to_predict = pd.DataFrame([payload.model_dump()])
#     clf = joblib.load(MODELS_PATH / "iris_classifier.joblib")
#     prediction = clf.predict(data_to_predict)
#     return {"predicted_flower": prediction[0]}