# TAXIPRED

**OPA24 OOP advanced 1**

## Taxi Fare Prediction App

## 1.  Project Overview

A full-stack machine learning project that predicts taxi fares based on trip details, weather, traffic, and other real-time factors. Built with FastAPI and Streamlit, using an XGBoost regression model trained on a Kaggle dataset.

## 2.  Tech Stack

- **Backend Framework**: FastAPI
- **Frontend Framework**: Streamlit
- **Model Type**: XGBoost (regression)
- **Data Source**: Kaggle – NYC Taxi Trip Pricing
- **APIs Used**:
  - Google Maps API (Distance, Geocoding, Directions)
  - OpenWeatherMap API (Weather conditions)
  - FastForex API (Currency conversion)

## 3.  Installation

- #### Clone the repository:
    ```bash
    git clone https://github.com/StefanLundberg77/taxi-prediction-fullstack-stefan-lundberg-opa24.git

-  #### Create and activate a virtual environment:
    uv venv # or other venv
    source venv\Scripts\activate # or .venv/bin/activate if mac

- #### Install dependencies:
    uv pip install -r requirements.txt

-  #### Install setuptools:
    uv pip install setuptools
    uv pip install -e .

- #### Set up your .env file with API keys:
    GOOGLE_MAPS_KEY=your_google_maps_api_key
    OPENWEATHER_API_KEY=your_openweather_api_key
    FASTFOREX_API_KEY=your_fastforex_api_key

- #### Start the backend:
    uvicorn taxipred.api:app --reload

- #### Launch the dashboard:
    streamlit run taxipred/dashboard.py

## 4.  **Usage**

- Enter pickup and destination addresses.
- Choose departure time and number of passengers.
- The app fetches distance, duration, traffic, and weather data.
- A machine learning model predicts the estimated fare in SEK.
- View route map, trip metrics, and prediction breakdown.

## 5. API Reference

##### API Endpoints

- `GET /api/` – Returns sample taxi trip data
- `POST /api/predict` – Accepts trip input and returns predicted price
- `GET /api/predict/missing_labels` – Predicts prices for rows missing labels

## 6. Project structure

```
├── 📂 explorations
│   ├── 📄 Cleaning_functions.py
│   ├── 📄 data_cleaning.ipynb
│   ├── 📄 eda.ipynb
│   ├── 📄 model.ipynb
│   ├── 📄 model_functions.py
│   └── 📂 __pycache__
│       ├── 📄 Cleaning_functions.cpython-313.pyc
│       ├── 📄 functions.cpython-313.pyc
│       └── 📄 model_functions.cpython-313.pyc
├── 📄 file_name.txt
├── 📄 README.md
├── 📄 requirements.txt
├── 📄 scratchbook.txt
├── 📄 setup.py
└── 📂 src
    ├── 📂 taxipred
    │   ├── 📂 backend
    │   │   ├── 📄 api.py
    │   │   ├── 📄 data_processing.py
    │   │   ├── 📄 __init__.py
    │   │   └── 📂 __pycache__
    │   │       ├── 📄 api.cpython-313.pyc
    │   │       ├── 📄 data_processing.cpython-313.pyc
    │   │       └── 📄 __init__.cpython-313.pyc
    │   ├── 📂 data
    │   │   ├── 📄 cleaned_data.csv
    │   │   └── 📄 taxi_trip_pricing.csv
    │   ├── 📂 frontend
    │   │   ├── 📄 dashboard.py
    │   │   └── 📄 __init__.py
    │   ├── 📂 models
    │   │   └── 📄 xgb_model.joblib
    │   ├── 📂 utils
    │   │   ├── 📄 constants.py
    │   │   ├── 📄 helpers.py
    │   │   ├── 📄 __init__.py
    │   │   └── 📂 __pycache__
    │   │       ├── 📄 constants.cpython-313.pyc
    │   │       ├── 📄 helpers.cpython-313.pyc
    │   │       └── 📄 __init__.cpython-313.pyc
    │   ├── 📄 __init__.py
    │   └── 📂 __pycache__
    │       └── 📄 __init__.cpython-313.pyc
    └── 📂 taxipred.egg-info
        ├── 📄 dependency_links.txt
        ├── 📄 PKG-INFO
        ├── 📄 requires.txt
        ├── 📄 SOURCES.txt
        └── 📄 top_level.txt
```


