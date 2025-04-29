import json
import os
import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

from weather_event import WeatherEvent
from weather_event_lambda import handler as event_handler
from weather_query_lambda import handler as query_handler


class TestWeatherEvent(unittest.TestCase):
    def test_weather_event_creation(self):
        event = WeatherEvent(
            location_name="New York",
            temperature=25.5,
            timestamp=1234567890,
            longitude=-74.0060,
            latitude=40.7128,
        )

        self.assertEqual(event.location_name, "New York")
        self.assertEqual(event.temperature, 25.5)
        self.assertEqual(event.timestamp, 1234567890)
        self.assertEqual(event.longitude, -74.0060)
        self.assertEqual(event.latitude, 40.7128)


class TestWeatherEventLambda(unittest.TestCase):
    def setUp(self):
        self.mock_table = MagicMock()
        self.mock_logger = MagicMock()
        self.table_patcher = patch("weather_event_lambda.table", self.mock_table)
        self.logger_patcher = patch("weather_event_lambda.logger", self.mock_logger)
        self.table_patcher.start()
        self.logger_patcher.start()
        # Set up environment variable
        os.environ["LOCATIONS_TABLE"] = "test-locations-table"

    def tearDown(self):
        self.table_patcher.stop()
        self.logger_patcher.stop()
        # Clean up environment variable
        del os.environ["LOCATIONS_TABLE"]

    def test_successful_event_processing(self):
        event = {
            "body": json.dumps(
                {
                    "location_name": "New York",
                    "temperature": "25.5",
                    "timestamp": "1234567890",
                    "longitude": "-74.0060",
                    "latitude": "40.7128",
                }
            )
        }

        response = event_handler(event, None)

        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(response["body"], "New York")
        self.mock_table.put_item.assert_called_once()

    def test_invalid_event_data(self):
        event = {
            "body": json.dumps(
                {
                    "location_name": "New York",
                    "temperature": "invalid",
                    "timestamp": "1234567890",
                    "longitude": "-74.0060",
                    "latitude": "40.7128",
                }
            )
        }

        response = event_handler(event, None)

        self.assertEqual(response["statusCode"], 500)
        self.assertIn("error", json.loads(response["body"]))
        self.mock_logger.exception.assert_called_once()


class TestWeatherQueryLambda(unittest.TestCase):
    def setUp(self):
        self.mock_table = MagicMock()
        self.mock_logger = MagicMock()
        self.table_patcher = patch("weather_query_lambda.table", self.mock_table)
        self.logger_patcher = patch("weather_query_lambda.logger", self.mock_logger)
        self.table_patcher.start()
        self.logger_patcher.start()
        # Set up environment variable
        os.environ["LOCATIONS_TABLE"] = "test-locations-table"

    def tearDown(self):
        self.table_patcher.stop()
        self.logger_patcher.stop()
        # Clean up environment variable
        del os.environ["LOCATIONS_TABLE"]

    def test_successful_query(self):
        mock_items = [
            {
                "locationName": "New York",
                "temperature": "25.5",
                "timestamp": "1234567890",
                "longitude": "-74.0060",
                "latitude": "40.7128",
            }
        ]
        self.mock_table.scan.return_value = {"Items": mock_items}

        event = {"queryStringParameters": {"limit": "10"}}
        response = query_handler(event, None)

        self.assertEqual(response["statusCode"], 200)
        result = json.loads(response["body"])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["location_name"], "New York")
        self.assertEqual(result[0]["temperature"], 25.5)

    def test_query_with_default_limit(self):
        mock_items = [
            {
                "locationName": "New York",
                "temperature": "25.5",
                "timestamp": "1234567890",
                "longitude": "-74.0060",
                "latitude": "40.7128",
            }
        ]
        self.mock_table.scan.return_value = {"Items": mock_items}

        event = {"queryStringParameters": None}
        response = query_handler(event, None)

        self.assertEqual(response["statusCode"], 200)
        result = json.loads(response["body"])
        self.assertEqual(len(result), 1)

    def test_query_error(self):
        self.mock_table.scan.side_effect = Exception("Database error")

        event = {"queryStringParameters": {"limit": "10"}}
        response = query_handler(event, None)

        self.assertEqual(response["statusCode"], 500)
        self.assertIn("error", json.loads(response["body"]))
        self.mock_logger.exception.assert_called_once()


if __name__ == "__main__":
    unittest.main()
