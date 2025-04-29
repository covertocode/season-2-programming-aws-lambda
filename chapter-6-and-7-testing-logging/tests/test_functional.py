import json
import os
from datetime import datetime

import boto3
import pytest
import requests

# Get the API endpoint from environment variable
API_ENDPOINT = os.getenv("API_ENDPOINT")

if not API_ENDPOINT:
    print("Error: API_ENDPOINT environment variable not set.")
    exit(1)

# Initialize DynamoDB client
dynamodb = boto3.resource("dynamodb")
table_name = os.getenv("LOCATIONS_TABLE", "LocationsTable")


def test_weather_event_lifecycle():
    # Test data
    test_location = {
        "locationName": "TestLocation",
        "temperature": 25.5,
        "timestamp": datetime.now().isoformat(),
        "humidity": 65,
    }

    # Step 1: Write data to the table via API
    response = requests.post(f"{API_ENDPOINT}/events", json=test_location)
    assert response.status_code == 200

    # Step 2: Verify data was written to DynamoDB
    table = dynamodb.Table(table_name)
    response = table.get_item(Key={"locationName": test_location["locationName"]})
    assert "Item" in response
    stored_item = response["Item"]

    # Verify the stored data matches what we sent
    assert stored_item["locationName"] == test_location["locationName"]
    assert float(stored_item["temperature"]) == test_location["temperature"]
    assert stored_item["humidity"] == test_location["humidity"]

    # Step 3: Query the data via API
    query_response = requests.get(f"{API_ENDPOINT}/locations")
    assert query_response.status_code == 200
    locations = query_response.json()
    assert any(
        loc["locationName"] == test_location["locationName"] for loc in locations
    )

    # Step 4: Clean up - delete the test data
    table.delete_item(Key={"locationName": test_location["locationName"]})

    # Verify the item was deleted
    response = table.get_item(Key={"locationName": test_location["locationName"]})
    assert "Item" not in response
