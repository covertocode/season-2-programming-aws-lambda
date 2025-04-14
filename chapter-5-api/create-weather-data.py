import json
import time
import os
import random
import http.client
import urllib.parse

# You'll still need to set the APP_URL environment variable
app_url = os.environ.get("APP_URL")

if not app_url:
    print("Error: APP_URL environment variable not set.")
    exit(1)

# Parse the URL to get host and path
parsed_url = urllib.parse.urlparse(app_url)
hostname = parsed_url.netloc
path = parsed_url.path + "/events"

locations = [
    {"name": "London, UK", "latitude": 51.51, "longitude": -0.13},
    {"name": "Paris, France", "latitude": 48.86, "longitude": 2.35},
    {"name": "Tokyo, Japan", "latitude": 35.68, "longitude": 139.76},
    {"name": "New York, USA", "latitude": 40.71, "longitude": -74.01},
    {"name": "Sydney, Australia", "latitude": -33.87, "longitude": 151.21},
    {"name": "Rome, Italy", "latitude": 41.90, "longitude": 12.50},
    {"name": "Berlin, Germany", "latitude": 52.52, "longitude": 13.40},
    {"name": "Cairo, Egypt", "latitude": 30.04, "longitude": 31.24},
    {"name": "Rio de Janeiro, Brazil", "latitude": -22.91, "longitude": -43.17},
    {"name": "Vancouver, Canada", "latitude": 49.28, "longitude": -123.12},
    {"name": "Amsterdam, Netherlands", "latitude": 52.37, "longitude": 4.90},
    {"name": "Seoul, South Korea", "latitude": 37.57, "longitude": 126.98},
    {"name": "Mexico City, Mexico", "latitude": 19.43, "longitude": -99.13},
    {"name": "Johannesburg, South Africa", "latitude": -26.20, "longitude": 28.04},
    {"name": "Stockholm, Sweden", "latitude": 59.33, "longitude": 18.07},
    {"name": "Buenos Aires, Argentina", "latitude": -34.60, "longitude": -58.37},
    {"name": "Singapore", "latitude": 1.35, "longitude": 103.82},
    {"name": "Hong Kong", "latitude": 22.32, "longitude": 114.17},
    {"name": "Istanbul, Turkey", "latitude": 41.01, "longitude": 28.98},
    {"name": "Bangkok, Thailand", "latitude": 13.75, "longitude": 100.50},
    {"name": "Anchorage, USA", "latitude": 61.2181, "longitude": -149.9003},
]

headers = {
    "Content-Type": "application/json"
}

for location_data in locations:
    temperature = random.randint(50, 85)
    timestamp = int(time.time())
    data = {
        "location_name": location_data["name"],
        "temperature": temperature,
        "timestamp": timestamp,
        "latitude": location_data["latitude"],
        "longitude": location_data["longitude"]
    }

    json_data = json.dumps(data)
    encoded_data = json_data.encode('utf-8')

    try:
        if parsed_url.scheme == "https":
            conn = http.client.HTTPSConnection(hostname)
        else:
            conn = http.client.HTTPConnection(hostname)

        conn.request("POST", path, body=encoded_data, headers=headers)
        response = conn.getresponse()

        print(f"Data posted for {location_data['name']}")
        print(f"Status: {response.status}, Reason: {response.reason}")
        response_data = response.read().decode('utf-8')
        if response_data:
            print(f"Response Data: {response_data}")
        conn.close()

    except Exception as e:
        print(f"Error posting data for {location_data['name']}: {e}")
    time.sleep(0.1)

print("Finished posting data for all locations.")
