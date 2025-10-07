from taxipred.utils.helpers import read_api_endpoint, post_api_endpoint, get_distance_duration, get_coordinates, display_map
from datetime import datetime
import streamlit as st
import pandas as pd

data = read_api_endpoint("/api")
df = pd.DataFrame(data.json())


def layout():
    st.markdown("# TAXIFY")

    # Initialize variables to avoid UnboundLocalError
    payload = None
    origin_lat = origin_lon = destination_lat = destination_lon = None

    with st.form("data"):
        origin = st.text_input("Pick up adress")
        destination = st.text_input("Destination adress")
        passenger_count = st.slider("Number of passangers", 1, 8, 2)
        submitted = st.form_submit_button("Get price prediction")

        # Show map inside form
        display_map(origin)


    if submitted:
        if origin and destination:
            distance_km, duration_min = get_distance_duration(origin, destination)
            if distance_km is not None and duration_min is not None:

                # Get coordinates from geocode API
                origin_lat, origin_lon = get_coordinates(origin)
                destination_lat, destination_lon = get_coordinates(destination)

                # Set current time
                now = datetime.now()

                # Prepare input payload for prediction
                payload = {
                    "Trip_Distance_km": distance_km,
                    "Trip_Duration_Minutes": duration_min,
                    "Time_of_Day_Afternoon": 12 <= now.hour < 18,
                    "Time_of_Day_Evening": 18 <= now.hour < 24,
                    "Passenger_Count": passenger_count,
                    "Day_of_Week_Weekday": now.weekday() < 5,
                    "Base_Fare": 3.5,
                    "Per_Km_Rate": 1.2,
                    "Per_Minute_Rate": 0.3,
                    "Traffic_Conditions_High": False,
                    "Weather_Rain": False,
                    "Weather_Snow": False
                }

                response = post_api_endpoint(payload, endpoint="/api/predict")
                if response.status_code == 200:
                    predicted_price = response.json().get("predicted_trip_price")

                    st.success(f"Price: {predicted_price} SEK")
                    st.info(f"Distance: {distance_km:.2f} km")
                    st.info(f"Travel time: {duration_min:.1f} minutes")
                else:
                    st.error("Unable to get predicted price")
            else:
                st.error("Unable to get distance or duration")
        else:
            st.warning("Enter pickup and destination")

    # Show payload if available
    with st.expander("Show payload"):
        if payload:
            st.json(payload)
        else:
            st.info("Unable to show payload.")

    # Show coordinates if available
    with st.expander("Show coordinates"):
        if origin_lat and origin_lon and destination_lat and destination_lon:
            st.info(f"Pick up coordinates = latitude: {origin_lat} longitude: {origin_lon}")
            st.info(f"Destination coordinates = latitude: {destination_lat} longitude: {destination_lon}")
        else:
            st.info("Unable to show coordinates.")
    
    with st.sidebar.expander("Dev options"):
            st.markdown("#### Raw data") # for testing
            st.dataframe(df)
        
        
#   cd src/taxipred/backend/
#   uvicorn  api:app --reload

#   cd src/taxipred/frontend/
#   streamlit run dashboard.py

if __name__ == '__main__':
    layout()

# start_time = st.slider(
#         "Boking",
#             value=datetime("YYYY", "DD", "MM", "hh", "mm"),
#             format="MM/DD/YY - hh:mm",
#         )
#         st.write("Start time:", start_time)


#                       count	mean	    std	        min	    25%	    50%	        75%	    max
# Trip_Distance_km	    1000.0	26.153327	15.521566	1.23	13.1075	26.995000	37.7825	74.795
# Base_Fare	            1000.0	3.502989	0.848107	2.01	2.7700	3.502989	4.2025	5.000
# Per_Km_Rate	        1000.0	1.233316	0.418922	0.50	0.8700	1.233316	1.5800	2.000
# Per_Minute_Rate	    1000.0	0.292916	0.112662	0.10	0.1975	0.292916	0.3825	0.500
# Trip_Duration_Minutes	1000.0	62.118116	31.339413	5.01	37.1075	62.118116	87.7750	119.840
# TODO:
#   - sätt uppstart requirements och förklara gällande api osv
#def get_request(url = base_url, endpoint):