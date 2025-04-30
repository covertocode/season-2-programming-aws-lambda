import json
import os
from typing import Any, Dict, List

import boto3
from aws_lambda_powertools import Logger, Metrics
from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_powertools.utilities.typing import LambdaContext

from weather_event import WeatherEvent

logger = Logger()
metrics = Metrics(namespace="WeatherData")

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["LOCATIONS_TABLE"])

DEFAULT_LIMIT = 50


def handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    try:
        query_params = event.get("queryStringParameters", {}) or {}
        logger.debug(f"Query parameters: {query_params}")

        limit = int(query_params.get("limit", DEFAULT_LIMIT))
        response = table.scan(Limit=limit)

        items = response["Items"]
        logger.info(f"Retrieved {len(items)} items from DynamoDB")

        weather_events = [
            WeatherEvent(
                location_name=item["locationName"],
                temperature=float(item["temperature"]),
                timestamp=int(item["timestamp"]),
                longitude=float(item["longitude"]),
                latitude=float(item["latitude"]),
            )
            for item in items
        ]
        logger.debug(f"Created {len(weather_events)} WeatherEvent objects")

        # Convert WeatherEvent objects to dictionaries for JSON serialization
        logger.debug("Converting WeatherEvent objects to dictionaries")
        weather_events_dict = [
            {
                "location_name": event.location_name,
                "temperature": event.temperature,
                "timestamp": event.timestamp,
                "longitude": event.longitude,
                "latitude": event.latitude,
            }
            for event in weather_events
        ]

        logger.info("Successfully processed query request")
        metrics.add_metric(name="SuccessfulEvents", unit=MetricUnit.Count, value=1)
        return {"statusCode": 200, "body": json.dumps(weather_events_dict)}
    except KeyError as e:
        logger.error(f"Missing required field in DynamoDB item: {str(e)}")
        metrics.add_metric(name="FailedEvents", unit=MetricUnit.Count, value=1)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Data integrity error: {str(e)}"}),
        }
    except ValueError as e:
        logger.error(f"Invalid data type in DynamoDB item: {str(e)}")
        metrics.add_metric(name="FailedEvents", unit=MetricUnit.Count, value=1)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Data type error: {str(e)}"}),
        }
    except Exception as e:
        logger.exception("Unexpected error querying weather events")
        metrics.add_metric(name="FailedEvents", unit=MetricUnit.Count, value=1)
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
