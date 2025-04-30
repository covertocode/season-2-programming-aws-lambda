import json
import os
from typing import Any, Dict

import boto3
from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_powertools.utilities.typing import LambdaContext

from weather_event import WeatherEvent

app = APIGatewayRestResolver()
logger = Logger()
tracer = Tracer()
metrics = Metrics(namespace="WeatherData")

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["LOCATIONS_TABLE"])


@app.get("/events")
@tracer.capture_method
def handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    try:
        weather_data = json.loads(event["body"])
        logger.debug(f"Parsed weather data: {weather_data}")

        weather_event = WeatherEvent(
            location_name=weather_data["location_name"],
            temperature=float(weather_data["temperature"]),
            timestamp=int(weather_data["timestamp"]),
            longitude=float(weather_data["longitude"]),
            latitude=float(weather_data["latitude"]),
        )

        item = {
            "locationName": weather_event.location_name,
            "temperature": str(weather_event.temperature),
            "timestamp": str(weather_event.timestamp),
            "longitude": str(weather_event.longitude),
            "latitude": str(weather_event.latitude),
        }
        logger.debug(f"DynamoDB item: {item}")

        table.put_item(Item=item)
        logger.info(
            f"Successfully wrote data for location: {weather_event.location_name}"
        )

        return {"statusCode": 200, "body": weather_event.location_name}
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse request body: {str(e)}")
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid JSON in request body"}),
        }
    except KeyError as e:
        logger.error(f"Missing required field in request: {str(e)}")
        return {
            "statusCode": 400,
            "body": json.dumps({"error": f"Missing required field: {str(e)}"}),
        }
    except ValueError as e:
        logger.error(f"Invalid data type in request: {str(e)}")
        return {
            "statusCode": 400,
            "body": json.dumps({"error": f"Invalid data type: {str(e)}"}),
        }
    except Exception as e:
        logger.exception("Unexpected error processing weather event")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
