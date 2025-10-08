from taxipred.utils.helpers import (
    read_api_endpoint, post_api_endpoint,
    get_trip_metrics, get_coordinates,
    get_map_directions, get_weather
)
from taxipred.utils.constants import ASSETS_PATH
from datetime import datetime, date
import streamlit as st
import pandas as pd

data = read_api_endpoint("/api")
df = pd.DataFrame(data.json())
image_path = ASSETS_PATH

def layout():

    # Add container with border
    with st.container(border=True):

        # splitting layout into two columns
        col1, col2 = st.columns([0.4, 0.6])#, border=True)
        
        # Initiate variables to avoid UnboundLocalError
        payload = None
        origin_lat = origin_lon = destination_lat = destination_lon = None
        predicted_price = None
        traffic_high = False
        distance_km = duration_min = None
        origin = destination = ""
        submitted = False
        response = None
        weather_rain = weather_snow = False

        with col1:

            # form with image, input boxes, and submit button
            with st.form("data"):
                st.image(image_path / "taxify.png")  
                origin = st.text_input("Pick up adress")
                destination = st.text_input("Destination adress")
                chosen_time = st.time_input("Time of departure", value="now")  # Default to 12:00 or now as a default?
                passenger_count = st.number_input("Number of passangers", 1, 8, 1)
                submitted = st.form_submit_button("Get estimated price", width="stretch")

                # Combine date and time into timestamp
                today = date.today()
                departure_datetime = datetime.combine(today, chosen_time)
                departure_timestamp = int(departure_datetime.timestamp())

            # If form successfully submitted
            if submitted:
                with st.spinner("Calculating route and price..."):
                    # if pick up address/destination submitted successfully else warning
                    if origin and destination:
    
                        # Get trip metrics (distance, duration, traffic)
                        distance_km, duration_min, traffic_high = get_trip_metrics(origin, destination, departure_timestamp)
                        if distance_km is None or duration_min is None:
                            st.error("Unable to get distance or duration")
                            return

                        # Get coordinates from geocode API
                        origin_lat, origin_lon = get_coordinates(origin)
                        destination_lat, destination_lon = get_coordinates(destination)
                        if None in [origin_lat, origin_lon, destination_lat, destination_lon]:
                            st.error("Unable to fetch coordinates for one or both addresses.")
                            return

                        # get weather from  openweather checking pickup and destination
                        origin_rain, origin_snow = get_weather(origin_lat, origin_lon)
                        destination_rain, destination_snow = get_weather(destination_lat, destination_lon)
                        weather_rain = origin_rain or destination_rain
                        weather_snow = origin_snow or destination_snow
                        
                        # set current time
                        now = datetime.now()

                        # set input payload for prediction
                        payload = {
                            "Trip_Distance_km": distance_km,
                            "Trip_Duration_Minutes": duration_min,
                            "Time_of_Day_Afternoon": 12 <= now.hour < 18,
                            "Time_of_Day_Evening": 18 <= now.hour < 24,
                            "Passenger_Count": passenger_count,
                            "Day_of_Week_Weekday": now.weekday() < 5,
                            "Base_Fare": 3.5,  # Mean
                            "Per_Km_Rate": 1.2,  # Mean
                            "Per_Minute_Rate": 0.3,  # Mean
                            "Traffic_Conditions_High": traffic_high,
                            "Weather_Rain": weather_rain,
                            "Weather_Snow": weather_snow
                        }

                        # Send payload to prediction API
                        response = post_api_endpoint(payload, endpoint="/api/predict")
                    else:
                        st.warning("Enter both pickup and destination")

        with col2:
            # Show map (either default or predicted route)
            if submitted and origin and destination:
                get_map_directions(origin, destination)
            else:
                get_map_directions("Göteborg, Sverige", "Göteborg, Sverige")
                
        if submitted:        
            with st.container(border=True):        
                if response and response.status_code == 200:
                    predicted_price = response.json().get("predicted_trip_price")
                    st.success(f"Price: {predicted_price} SEK")
                    st.info(f"Distance: {distance_km:.2f} km")
                    st.info(f"Travel time: {duration_min:.1f} minutes")
                    st.info(f"Traffic: {'High' if traffic_high else 'Normal'}")
                    
                    # list for rain or snow weather
                    weather_status = []
                    if weather_rain:
                        weather_status.append("Raining")
                    if weather_snow:
                        weather_status.append("Snowing")
                        
                    # concatenate if both rain and snow
                    if weather_status:
                        st.info(f"Weather: {', '.join(weather_status) if weather_status else 'Normal'}")
                else:
                    st.error("Unable to get predicted price")   
                    

    # Sidebar with raw data for testing?
    with st.sidebar.expander("Dev options"):
        # Show payload if available
        if submitted:
            with st.expander("Show payload"):
                if payload:
                    st.json(payload)
                else:
                    st.info("Unable to show payload. Enter pickup and destination")

            # Show coordinates if available
            with st.expander("Show coordinates"):
                if None not in [origin_lat, origin_lon, destination_lat, destination_lon]:
                    st.info(f"Pick up coordinates = latitude: {origin_lat} longitude: {origin_lon}")
                    st.info(f"Destination coordinates = latitude: {destination_lat} longitude: {destination_lon}")
                else:
                    st.info("Unable to show coordinates. Enter pickup and destination")
        
        st.markdown("#### Raw data")
        st.dataframe(df)

if __name__ == '__main__':
    layout()

# TODO:
#   - Weather
#   - Kpi?
#   - passangers count for statistics
#   - trip count or submit count?

#   cd src/taxipred/backend/
#   uvicorn  api:app --reload

#   cd src/taxipred/frontend/
#   streamlit run dashboard.py

# start_time = st.slider(
#         "Boking",
#             value=datetime("YYYY", "DD", "MM", "hh", "mm"),
#             format="MM/DD/YY - hh:mm",
#         )
#         st.write("Start time:", start_time)

# Feat– feature

# Fix– bug fixes

# Docs– changes to the documentation like README

# Style– style or formatting change 

# Perf – improves code performance

# Test– test a feature

# Summary:

# Docs: Fixes typo on in-from-the-depths.md