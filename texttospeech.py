import requests
import json

# Define the API endpoint URL
url = 'http://192.168.137.137:4000/text-to-speech'


# Define the text to convert to speech
text = 'Emergency come out of the mines'

# Define the JSON payload for the POST request
payload = {'text': text}

# Make the POST request
response = requests.post(url, json=payload)

# Check if the request was successful
if response.status_code == 200:
    print('Audio played successfully')
else:
    print(f'Error: {response.json()["error"]}')