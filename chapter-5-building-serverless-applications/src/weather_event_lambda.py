import json
import os
from typing import Any, Dict

import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger()
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['LOCATIONS_TABLE'])

def handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    try:
        weather_event = json.loads(event['body'])

        table.put_item(
            Item={
                'locationName': weather_event['location_name'],
                'temperature': weather_event['temperature'],
                'timestamp': weather_event['timestamp'],
                'longitude': weather_event['longitude'],
                'latitude': weather_event['latitude']
            }
        )

        return {
            'statusCode': 200,
            'body': weather_event['location_name']
        }
    except Exception as e:
        logger.exception("Error processing weather event")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
