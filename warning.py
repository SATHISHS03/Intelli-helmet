import requests
import streamlit as st
import time
import cv2
import pandas as pd
import altair as alt
st.set_page_config(page_title="Real-Time Data Visualization")
url = "http://192.168.137.137:8080/"
cap = cv2.VideoCapture(url)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
if not cap.isOpened():
    st.error("Error opening video stream")

st.title("Real-Time Data Visualization and Video Stream Demo")
st.header("Live Video Stream")
st.write("")
st.write("")
def text_to_speech(text):
    url = 'http://192.168.137.137:4000/text-to-speech'
    # Define the JSON payload for the POST request
    payload = {'text': text}

    # Make the POST request
    response = requests.post(url, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        st.success('Audio played successfully')
    else:
        st.error(f'Error: {response.json()["error"]}')

stframe = st.empty()
st.sidebar.subheader("Live Sensor Data")


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

chart_temperature = chart_temperature.properties(height=300)
chart_humidity = chart_humidity.properties(height=300)
st.container([chart_temperature, chart_humidity])
))


# create sidebar to display live temperature and humidity values
st.sidebar.title("Live Values")
live_temperature = st.sidebar.text("Temperature (°C):")
live_humidity = st.sidebar.text("Humidity (%):")
live_quality_status = st.sidebar.text("Air Quality :")

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
        
        # update live temperature and humidity values
        live_temperature.text("Temperature (°C): {}".format(temperature))
        live_humidity.text("Humidity (%): {}".format(humidity))
        live_quality_status.text("Air Quality : {}".format(air_quality_status))
        
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
        
        # check for hazardous gas and display warning
        if air_quality_status == 'Hazardous Gas detected':
            st.warning('Gas detected')
        else:
            pass
    ret, frame = cap.read()
    if not ret:
        st.error("Error reading frame from video stream")
        break
    stframe.image(frame, channels="BGR")

cap.release()

