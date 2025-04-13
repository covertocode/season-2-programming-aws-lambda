import json
import os
from typing import Any, Dict

import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

from weather_event import WeatherEvent

logger = Logger()
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['LOCATIONS_TABLE'])

def handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    try:
        weather_data = json.loads(event['body'])
        weather_event = WeatherEvent(
            location_name=weather_data['location_name'],
            temperature=float(weather_data['temperature']),
            timestamp=int(weather_data['timestamp']),
            longitude=float(weather_data['longitude']),
            latitude=float(weather_data['latitude'])
        )

        table.put_item(
            Item={
                'locationName': weather_event.location_name,
                'temperature': str(weather_event.temperature),
                'timestamp': str(weather_event.timestamp),
                'longitude': str(weather_event.longitude),
                'latitude': str(weather_event.latitude)
            }
        )

        return {
            'statusCode': 200,
            'body': weather_event.location_name
        }
    except Exception as e:
        logger.exception("Error processing weather event")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
