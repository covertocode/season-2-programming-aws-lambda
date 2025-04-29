import http.client
import json
import os
import random
import time
import urllib.parse

# Get the API endpoint from environment variable
API_ENDPOINT = os.getenv("API_ENDPOINT")

if not API_ENDPOINT:
    print("Error: API_ENDPOINT environment variable not set.")
    exit(1)

# Parse the URL to get host and path
parsed_url = urllib.parse.urlparse(API_ENDPOINT)
hostname = parsed_url.netloc
path = parsed_url.path + "/events"

locations = [
    {"name": "Amsterdam, Netherlands", "latitude": 52.37, "longitude": 4.90},
    {"name": "Anchorage, USA", "latitude": 61.2181, "longitude": -149.9003},
    {"name": "Austin, USA", "latitude": 30.2672, "longitude": -97.7431},
    {"name": "Bangalore, India", "latitude": 12.9716, "longitude": 77.5903},
    {"name": "Bangkok, Thailand", "latitude": 13.75, "longitude": 100.50},
    {"name": "Beijing, China", "latitude": 39.9042, "longitude": 116.4074},
    {"name": "Berlin, Germany", "latitude": 52.52, "longitude": 13.40},
    {"name": "Bogota, Colombia", "latitude": 4.6097, "longitude": -74.0817},
    {"name": "Buenos Aires, Argentina", "latitude": -34.60, "longitude": -58.37},
    {"name": "Buenos Aires, Argentina", "latitude": -34.6037, "longitude": -58.3816},
    {"name": "Cairo, Egypt", "latitude": 30.04, "longitude": 31.24},
    {"name": "Calgary, Canada", "latitude": 51.0447, "longitude": -114.0719},
    {"name": "Chennai, India", "latitude": 13.0827, "longitude": 80.2707},
    {"name": "Chicago, USA", "latitude": 41.8781, "longitude": -87.6298},
    {"name": "Chongqing, China", "latitude": 29.5630, "longitude": 106.5516},
    {"name": "Dallas, USA", "latitude": 32.7767, "longitude": -96.7970},
    {"name": "Delhi, India", "latitude": 28.7041, "longitude": 77.1025},
    {"name": "Guangzhou, China", "latitude": 23.1291, "longitude": 113.2644},
    {"name": "Hong Kong", "latitude": 22.32, "longitude": 114.17},
    {"name": "Houston, USA", "latitude": 29.7604, "longitude": -95.3698},
    {"name": "Istanbul, Turkey", "latitude": 41.01, "longitude": 28.98},
    {"name": "Johannesburg, South Africa", "latitude": -26.20, "longitude": 28.04},
    {"name": "Kolkata, India", "latitude": 22.5726, "longitude": 88.3639},
    {"name": "Lima, Peru", "latitude": -12.0464, "longitude": -77.0428},
    {"name": "London, UK", "latitude": 51.51, "longitude": -0.13},
    {"name": "Los Angeles, USA", "latitude": 34.0522, "longitude": -118.2437},
    {"name": "Mexico City, Mexico", "latitude": 19.43, "longitude": -99.13},
    {"name": "Montreal, Canada", "latitude": 45.5017, "longitude": -73.5673},
    {"name": "Mumbai, India", "latitude": 19.0760, "longitude": 72.8777},
    {"name": "New York, USA", "latitude": 40.71, "longitude": -74.01},
    {"name": "Ottawa, Canada", "latitude": 45.4215, "longitude": -75.6972},
    {"name": "Paris, France", "latitude": 48.86, "longitude": 2.35},
    {"name": "Philadelphia, USA", "latitude": 39.9526, "longitude": -75.1652},
    {"name": "Phoenix, USA", "latitude": 33.4484, "longitude": -112.0739},
    {"name": "Rio de Janeiro, Brazil", "latitude": -22.91, "longitude": -43.17},
    {"name": "Rome, Italy", "latitude": 41.90, "longitude": 12.50},
    {"name": "San Diego, USA", "latitude": 32.7157, "longitude": -117.1611},
    {"name": "San Francisco, USA", "latitude": 37.7749, "longitude": -122.4194},
    {"name": "Santiago, Chile", "latitude": -33.4489, "longitude": -70.6693},
    {"name": "Sao Paulo, Brazil", "latitude": -23.5505, "longitude": -46.6333},
    {"name": "Seattle, USA", "latitude": 47.6062, "longitude": -122.3321},
    {"name": "Seoul, South Korea", "latitude": 37.57, "longitude": 126.98},
    {"name": "Shanghai, China", "latitude": 31.2304, "longitude": 121.4737},
    {"name": "Shenzhen, China", "latitude": 22.5431, "longitude": 114.0579},
    {"name": "Singapore", "latitude": 1.35, "longitude": 103.82},
    {"name": "Stockholm, Sweden", "latitude": 59.33, "longitude": 18.07},
    {"name": "Sydney, Australia", "latitude": -33.87, "longitude": 151.21},
    {"name": "Tokyo, Japan", "latitude": 35.68, "longitude": 139.76},
    {"name": "Toronto, Canada", "latitude": 43.6532, "longitude": -79.3832},
    {"name": "Vancouver, Canada", "latitude": 49.28, "longitude": -123.12},
    {"name": "Vancouver, Canada", "latitude": 49.2827, "longitude": -123.1207},
]

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
