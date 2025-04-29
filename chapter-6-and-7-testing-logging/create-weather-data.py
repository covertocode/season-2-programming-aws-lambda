import http.client
import json
import os
import random
import time
import urllib.parse
import sys


# Get the API endpoint from environment variable
API_ENDPOINT = os.getenv("API_ENDPOINT")

if not API_ENDPOINT:
    print("Error: API_ENDPOINT environment variable not set.")
    exit(1)

# Get the Weather Data file from environment variable or use default
WEATHER_DATA_FILE = os.getenv("WEATHER_DATA_FILE", "weather_data.json")

# Read locations from JSON file
try:
    with open(WEATHER_DATA_FILE, 'r') as f:
        locations = json.load(f)
except FileNotFoundError:
    print(f"Error: Weather data file '{WEATHER_DATA_FILE}' not found.")
    exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON in weather data file '{WEATHER_DATA_FILE}'.")
    exit(1)

# Parse the URL to get host and path
parsed_url = urllib.parse.urlparse(API_ENDPOINT)
hostname = parsed_url.netloc
path = parsed_url.path + "/events"

headers = {"Content-Type": "application/json"}

print(f"Posting data for {len(locations)} locations to {API_ENDPOINT}...")

for location_data in locations:
    temperature = random.randint(50, 85)
    timestamp = int(time.time())
    data = {
        "location_name": location_data["name"],
        "temperature": temperature,
        "timestamp": timestamp,
        "latitude": location_data["latitude"],
        "longitude": location_data["longitude"],
    }

    json_data = json.dumps(data)
    encoded_data = json_data.encode("utf-8")

    try:
        if parsed_url.scheme == "https":
            conn = http.client.HTTPSConnection(hostname)
        else:
            conn = http.client.HTTPConnection(hostname)

        conn.request("POST", path, body=encoded_data, headers=headers)
        response = conn.getresponse()

        print(f"Status: {response.status}, Reason: {response.reason}", end=" ")

        response_data = response.read().decode("utf-8")

        if response_data:
            print(f"Response Data: {response_data}")
        conn.close()

    except Exception as e:
        print(f"Error posting data for {location_data['name']}: {e}")
    time.sleep(0.1)

print("Finished posting data for all locations.")
