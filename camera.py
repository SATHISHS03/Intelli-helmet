import cv2
import numpy as np
import streamlit as st

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

# Start the Streamlit app
def main():
    st.title("Video Stream Demo")
    st.header("Live Video Stream")
    url = "http://192.168.137.137:8080/"
    video_stream = read_stream(url)
    stframe = st.empty()
    for frame in video_stream:
        stframe.image(frame, channels="BGR")
if __name__ == "__main__":
    main()
