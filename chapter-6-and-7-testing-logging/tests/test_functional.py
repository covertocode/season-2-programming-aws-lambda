import json
import os
from datetime import datetime
import unittest
import http.client
import urllib.parse

import boto3

# Get the API endpoint from environment variable
API_ENDPOINT = os.getenv("API_ENDPOINT")

if not API_ENDPOINT:
    print("Error: API_ENDPOINT environment variable not set.")
    exit(1)

# Parse the URL to get host and path
parsed_url = urllib.parse.urlparse(API_ENDPOINT)
hostname = parsed_url.netloc
base_path = parsed_url.path

# Initialize DynamoDB client
dynamodb = boto3.resource("dynamodb")
table_name = os.getenv("LOCATIONS_TABLE", "LocationsTable")


class TestWeatherEventLifecycle(unittest.TestCase):
    def setUp(self):
        """Set up test data before each test"""
        self.test_location = {
            "locationName": "TestLocation",
            "temperature": 25.5,
            "timestamp": datetime.now().isoformat(),
            "humidity": 65,
        }
        self.table = dynamodb.Table(table_name)
        self.headers = {"Content-Type": "application/json"}

    def tearDown(self):
        """Clean up test data after each test"""
        try:
            self.table.delete_item(Key={"locationName": self.test_location["locationName"]})
        except Exception:
            pass

    def make_request(self, method, path, data=None):
        """Helper method to make HTTP requests"""
        if parsed_url.scheme == "https":
            conn = http.client.HTTPSConnection(hostname)
        else:
            conn = http.client.HTTPConnection(hostname)

        try:
            if data:
                json_data = json.dumps(data)
                encoded_data = json_data.encode("utf-8")
                conn.request(method, path, body=encoded_data, headers=self.headers)
            else:
                conn.request(method, path, headers=self.headers)

            response = conn.getresponse()
            response_data = response.read().decode("utf-8")
            return response.status, response_data
        finally:
            conn.close()

    def test_weather_event_lifecycle(self):
        # Step 1: Write data to the table via API
        status_code, _ = self.make_request("POST", f"{base_path}/events", self.test_location)
        self.assertEqual(status_code, 200)

        # Step 2: Verify data was written to DynamoDB
        response = self.table.get_item(Key={"locationName": self.test_location["locationName"]})
        self.assertIn("Item", response)
        stored_item = response["Item"]

        # Verify the stored data matches what we sent
        self.assertEqual(stored_item["locationName"], self.test_location["locationName"])
        self.assertEqual(float(stored_item["temperature"]), self.test_location["temperature"])
        self.assertEqual(stored_item["humidity"], self.test_location["humidity"])

        # Step 3: Query the data via API
        status_code, response_data = self.make_request("GET", f"{base_path}/locations")
        self.assertEqual(status_code, 200)
        locations = json.loads(response_data)
        self.assertTrue(
            any(loc["locationName"] == self.test_location["locationName"] for loc in locations)
        )

        # Step 4: Clean up is handled by tearDown method


if __name__ == '__main__':
    unittest.main()
