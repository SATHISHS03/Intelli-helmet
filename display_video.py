import cv2

# Open the video stream from the URL
cap = cv2.VideoCapture('http://192.168.43.217:8080/')

# Check if the stream was opened successfully
if not cap.isOpened():
    print("Error opening video stream")

# Loop through the frames in the stream
while True:
    # Read the next frame from the stream
    ret, frame = cap.read()

    # Check if the frame was read successfully
    if not ret:
        print("Error reading frame from video stream")
        break

    # Display the frame in a window
    cv2.imshow('Video Stream', frame)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video stream and close the window
cap.release()
cv2.destroyAllWindows()