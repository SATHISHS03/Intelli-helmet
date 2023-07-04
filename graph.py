import requests
import streamlit as st
import time
import pandas as pd
import altair as alt

st.set_page_config(page_title="Real-Time Data Visualization")

# create empty DataFrames to store data
temperature_df = pd.DataFrame(columns=["Time", "Temperature (°C)"])
humidity_df = pd.DataFrame(columns=["Time", "Humidity (%)"])

# create line charts to display data
col1, col2 = st.columns(2)

chart_temperature = col1.altair_chart(alt.Chart(temperature_df).mark_line().encode(
    x='Time',
    y='Temperature (°C)',
    tooltip=['Time', 'Temperature (°C)']
).properties(
    width=400,
    height=300
))

chart_humidity = col2.altair_chart(alt.Chart(humidity_df).mark_line().encode(
    x='Time',
    y='Humidity (%)',
    tooltip=['Time', 'Humidity (%)']
).properties(
    width=400,
    height=300
))

while True:
    response = requests.get('http://192.168.137.137:5000/')
    if response.status_code == 200:
        data = response.json()
        air_quality_status = data["air_quality_status"]
        temperature = data["temperature"]
        humidity = data["humidity"]
        current_time = time.strftime("%H:%M:%S", time.localtime())
        temperature_df.loc[len(temperature_df)] = [current_time, temperature]
        humidity_df.loc[len(humidity_df)] = [current_time, humidity]
        chart_temperature.altair_chart(alt.Chart(temperature_df).mark_line().encode(
            x='Time',
            y='Temperature (°C)',
            tooltip=['Time', 'Temperature (°C)']
        ).properties(
            width=400,
            height=300
        ))
        chart_humidity.altair_chart(alt.Chart(humidity_df).mark_line().encode(
            x='Time',
            y='Humidity (%)',
            tooltip=['Time', 'Humidity (%)']
        ).properties(
            width=400,
            height=300
        ))
