import json
import os
from datetime import datetime
import unittest

import boto3
import requests

# Get the API endpoint from environment variable
API_ENDPOINT = os.getenv("API_ENDPOINT")

if not API_ENDPOINT:
    print("Error: API_ENDPOINT environment variable not set.")
    exit(1)

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

    def tearDown(self):
        """Clean up test data after each test"""
        try:
            self.table.delete_item(Key={"locationName": self.test_location["locationName"]})
        except Exception:
            pass

    def test_weather_event_lifecycle(self):
        # Step 1: Write data to the table via API
        response = requests.post(f"{API_ENDPOINT}/events", json=self.test_location)
        self.assertEqual(response.status_code, 200)

        # Step 2: Verify data was written to DynamoDB
        response = self.table.get_item(Key={"locationName": self.test_location["locationName"]})
        self.assertIn("Item", response)
        stored_item = response["Item"]

        # Verify the stored data matches what we sent
        self.assertEqual(stored_item["locationName"], self.test_location["locationName"])
        self.assertEqual(float(stored_item["temperature"]), self.test_location["temperature"])
        self.assertEqual(stored_item["humidity"], self.test_location["humidity"])

        # Step 3: Query the data via API
        query_response = requests.get(f"{API_ENDPOINT}/locations")
        self.assertEqual(query_response.status_code, 200)
        locations = query_response.json()
        self.assertTrue(
            any(loc["locationName"] == self.test_location["locationName"] for loc in locations)
        )

        # Step 4: Clean up is handled by tearDown method


if __name__ == '__main__':
    unittest.main()
