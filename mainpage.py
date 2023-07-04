import streamlit as st
import requests
import base64

global livetemperature
global livehumidity
global livequalitystatus

st.sidebar.title("Intelli - helmet")

pages = ["Live Graph", "Live Feed"]
st.markdown(' ')
selection = st.sidebar.radio("Navigation", pages)
# Create the sidebar widgets
st.sidebar.title('Emergency Message')
message = st.sidebar.text_input('Enter your message:')
button = st.sidebar.button('Send')

url = 'http://192.168.137.137:4000/text-to-speech'
payload = {'text': message}
response = requests.post(url, json=payload)
if response.status_code == 200:
    st.success('Audio played successfully')


def graph_page():
    import requests
    import time
    import pandas as pd
    import altair as alt
    global livetemperature
    global temperature
    global humidity
    global air_quality_status
    global livehumidity
    global livequalitystatus

    st.title("Intelli - Helmet")

    # create empty DataFrames to store data
    temperature_df = pd.DataFrame(columns=["Time", "Temperature (°C)"])
    humidity_df = pd.DataFrame(columns=["Time", "Humidity (%)"])
    
    livetemperature = st.text("Temperature (°C):")
    livehumidity = st.text("Humidity (%):")
    livequalitystatus = st.text("Air Quality :")
    chart_temperature = st.empty()
    chart_humidity = st.empty()
    

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
                width=700,
                height=500
            ))
            chart_humidity.altair_chart(alt.Chart(humidity_df).mark_line().encode(
                x='Time',
                y='Humidity (%)',
                tooltip=['Time', 'Humidity (%)']
            ).properties(
                width=700,
                height=500
            ))
        if air_quality_status != "Fine" :
            event = f'intelli_helmet_air'
            URL = f"https://maker.ifttt.com/trigger/{event}/json/with/key/dmijtABpP4rpt_SHHapVHJ"
            req = requests.get(url = URL)
        elif temperature >= 31:
            event = f'intelli_helmet_temperature'
            URL = f"https://maker.ifttt.com/trigger/{event}/json/with/key/dmijtABpP4rpt_SHHapVHJ"
            req = requests.get(url = URL)

        livetemperature.text("Temperature (°C): {}".format(temperature))
        livehumidity.text("Humidity (%): {}".format(humidity))
        livequalitystatus.text("Air Quality : {}".format(air_quality_status)) 
       
        

    
def camera_page():
    global livetemperature
    global livehumidity
    global livequalitystatus

    import cv2
    import numpy as np
    st.title("Intelli - Helmet")
    # Function to read the video stream and return a frame
    def read_stream(url):
        cap = cv2.VideoCapture(url)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        if not cap.isOpened():
            st.error("Error opening video stream")
        while True:
            ret, frame = cap.read()
            if not ret:
                st.error("Error reading frame from video stream")
                break
            yield frame
        
    url = "http://192.168.137.137:8080/"
    video_stream = read_stream(url)
    stframe = st.empty()
    for frame in video_stream:
        stframe.image(frame, channels="BGR")

if selection == "Live Graph":
    graph_page()
elif selection == "Live Feed":
    camera_page()

