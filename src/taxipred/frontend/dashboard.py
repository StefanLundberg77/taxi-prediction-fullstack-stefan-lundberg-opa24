from taxipred.utils.helpers import read_api_endpoint, post_api_endpoint, get_distance_duration
from datetime import datetime
import streamlit as st
import pandas as pd

data = read_api_endpoint("/api")
df = pd.DataFrame(data.json())


def layout():
    st.markdown("""
    <style>
    body {
        background-color: #1e1e1e;
        color: white;
    }
    </style>
    """,
        unsafe_allow_html=True
    )
    
    

    st.markdown("""
                :red[Streamlit] :orange[can] :green[write] :blue[text] :violet[in]
                """
    )    
    with st.form("data"):
        origin = st.text_input("Pick up adress")
        destination = st.text_input("Destination adress")
        submitted = st.form_submit_button("Get price prediction") # add func so it doens crash if not input
    
    if submitted:
        if origin and destination:
            distance_km, duration_min = get_distance_duration(origin, destination)
            if distance_km is not None and duration_min is not None:
                st.success(f"Distance: {distance_km:.2f} km")
                st.info(f"Travel time: {duration_min:.1f} minutes")
                now = datetime.now()
                payload = {
                        "Trip_Distance_km": distance_km,
                        "Trip_Duration_Minutes": duration_min,
                        "Time_of_Day_Afternoon": 12 <= now.hour < 18,
                        "Day_of_Week_Weekday": now.weekday() < 5,
                        "Base_Fare": 3.5,
                        "Per_Km_Rate": 1.2,
                        "Per_Minute_Rate": 0.3,
                        "Passenger_Count": 2,
                        "Traffic_Conditions_High": False,
                        "Weather_Rain": False,
                        "Weather_Snow": False
                    }
        #response = post_api_endpoint(payload, endpoint="/api/predict")
        #predicted_ = response.json().get("predicted_")
        response = post_api_endpoint(payload, endpoint="/api/predict")
        if response.status_code == 200:
            predicted_price = response.json().get("predicted_trip_price")
            st.success(f"Price: {predicted_price} SEK")
        else:
            st.error("Unable to get predicted price")
    else:
        st.warning("Enter pickup/destination")
    
    # st.sidebar.title("""
    #                  :red[Settings]
    #                  """)
    # Passenger_Count = st.sidebar.slider("Number of passangers", 1, 6, 2)
    
    
    # st.markdown("## Raw data") # for testing
    # st.dataframe(df)


if __name__ == '__main__':
    layout()

#                       count	mean	    std	        min	    25%	    50%	        75%	    max
# Trip_Distance_km	    1000.0	26.153327	15.521566	1.23	13.1075	26.995000	37.7825	74.795
# Base_Fare	            1000.0	3.502989	0.848107	2.01	2.7700	3.502989	4.2025	5.000
# Per_Km_Rate	        1000.0	1.233316	0.418922	0.50	0.8700	1.233316	1.5800	2.000
# Per_Minute_Rate	    1000.0	0.292916	0.112662	0.10	0.1975	0.292916	0.3825	0.500
# Trip_Duration_Minutes	1000.0	62.118116	31.339413	5.01	37.1075	62.118116	87.7750	119.840
# TODO:
#   - sätt uppstart requirements och förklara gällande api osv
#def get_request(url = base_url, endpoint):