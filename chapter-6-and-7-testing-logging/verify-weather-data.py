#!/usr/bin/env python3
import json
import os
import sys

import requests

print("# Reading configuration...")
# Get the API endpoint from environment variable
API_ENDPOINT = os.getenv("API_ENDPOINT")
if not API_ENDPOINT:
    print("Error: API_ENDPOINT environment variable not set.")
    sys.exit(1)

# Get the Weather Data file from environment variable or use default
WEATHER_DATA_FILE = os.getenv("WEATHER_DATA_FILE", "weather_data.json")
print(f"# Using weather data file: {WEATHER_DATA_FILE}")

print("# Reading expected locations from JSON file...")
# Read expected locations from JSON file
try:
    with open(WEATHER_DATA_FILE, "r") as f:
        expected_locations = json.load(f)
    print(f"# Successfully loaded {len(expected_locations)} expected locations")
except FileNotFoundError:
    print(f"Error: Weather data file '{WEATHER_DATA_FILE}' not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON in weather data file '{WEATHER_DATA_FILE}'.")
    sys.exit(1)

print("# Fetching locations from API...")
# Get locations from the API
try:
    response = requests.get(f"{API_ENDPOINT}/locations")
    if response.status_code != 200:
        print(f"Error: Failed to get locations. Status code: {response.status_code}")
        sys.exit(1)

    actual_locations = response.json()
    print(f"# Successfully retrieved {len(actual_locations)} locations from API")
except requests.exceptions.RequestException as e:
    print(f"Error: Failed to connect to API: {e}")
    sys.exit(1)

# Verify we have data
if not actual_locations:
    print("Error: No locations returned from API")
    sys.exit(1)

print("# Creating location lookup map...")
# Create a map of expected locations by name for easier lookup
expected_map = {loc["name"]: loc for loc in expected_locations}

print("# Starting verification of locations...")
# Verify each location from the API
errors = []
for actual_loc in actual_locations:
    name = actual_loc["location_name"]
    print(f"# Verifying location: {name}")

    if name not in expected_map:
        errors.append(f"Unexpected location in API: {name}")
        continue

    expected_loc = expected_map[name]

    # Verify coordinates match (allowing for small floating point differences)
    if not (
        abs(float(actual_loc["latitude"]) - float(expected_loc["latitude"])) < 0.01
        and abs(float(actual_loc["longitude"]) - float(expected_loc["longitude"]))
        < 0.01
    ):
        errors.append(
            f"Coordinates mismatch for {name}: "
            f"expected ({expected_loc['latitude']}, {expected_loc['longitude']}), "
            f"got ({actual_loc['latitude']}, {actual_loc['longitude']})"
        )

    # Verify required fields are present
    required_fields = ["temperature", "timestamp"]
    for field in required_fields:
        if field not in actual_loc:
            errors.append(f"Missing required field '{field}' for location {name}")

print("# Checking for missing locations...")
# Check if any locations are missing from the API
actual_names = {loc["location_name"] for loc in actual_locations}
expected_names = {loc["name"] for loc in expected_locations}
missing_locations = expected_names - actual_names
if missing_locations:
    errors.append(f"Locations missing from API: {', '.join(missing_locations)}")

# Report results
if errors:
    print("\n# Verification failed with the following errors:")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)
else:
    print("\n# All verifications passed successfully!")
    print(f"# Verified {len(actual_locations)} locations match the expected data.")
    print("# All coordinates match within tolerance")
    print("# All required fields are present")
    print("# No missing or unexpected locations found")
