import streamlit as st
import pandas as pd
from src.taxipred.utils.helpers import read_api_endpoint, post_api_endpoint

data = read_api_endpoint("/api")
df = pd.DataFrame(data.json())

# TODO: try to predict...

def layout():
    st.markdown("# ")
    st.markdown("## Raw data")
    st.dataframe(df)
    
    with st.form("data"):
        placeholder = st.number_input(
            "placeholder", min_value=4, max_value=9,
        )
        submitted = st.form_submit_button("Predict")
    
    if submitted:
        payload = {}
        
    response = post_api_endpoint(payload, endpoint="/api/predict")
    predicted_ = response.json().get("predicted_")
    
    st.markdown(f"predicted_: {predicted_}")


if __name__ == '__main__':
    layout()

#def get_request(url = base_url, endpoint):