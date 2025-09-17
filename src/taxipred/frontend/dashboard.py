import streamlit as st
from taxipred.utils.helpers import read_api_endpoint
import pandas as pd


data = read_api_endpoint("taxi")

df = pd.DataFrame(data.json()) # converts api response -> list of json dicts


def main():
    st.markdown("# Taxi Prediction Dashboard")

    st.dataframe(df)


if __name__ == "__main__":
    main()
