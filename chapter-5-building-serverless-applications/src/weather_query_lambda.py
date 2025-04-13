import json
import os
from typing import Any, Dict, List

import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger()
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['LOCATIONS_TABLE'])

DEFAULT_LIMIT = 50

def handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    try:
        query_params = event.get('queryStringParameters', {}) or {}
        limit = int(query_params.get('limit', DEFAULT_LIMIT))

        response = table.scan(Limit=limit)
        items = response['Items']

        weather_events = [
            {
                'location_name': item['locationName'],
                'temperature': float(item['temperature']),
                'timestamp': int(item['timestamp']),
                'longitude': float(item['longitude']),
                'latitude': float(item['latitude'])
            }
            for item in items
        ]

        return {
            'statusCode': 200,
            'body': json.dumps(weather_events)
        }
    except Exception as e:
        logger.exception("Error querying weather events")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
