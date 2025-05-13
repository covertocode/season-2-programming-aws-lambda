import json
import boto3
import os
import datetime
import uuid

# Get environment variables
TABLE_NAME = os.environ['TABLE_NAME']
REGION = os.environ['REGION']
DEFAULT_ID = os.environ.get('DEFAULT_ID', 'default-item-id')

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name=REGION)
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    """
    Lambda function that writes to the DynamoDB Global Table.
    For each GET/POST request, the function writes event and context details
    to the table using a fixed ID.
    """
    try:
        # Get current timestamp
        timestamp = datetime.datetime.utcnow().isoformat()

        # Extract method and path from event
        request_context = event.get('requestContext', {})
        http_method = request_context.get('http', {}).get('method', 'UNKNOWN')
        path = request_context.get('http', {}).get('path', 'UNKNOWN')
        source_ip = request_context.get('http', {}).get('sourceIp', 'UNKNOWN')

        # Get basic context information
        request_id = context.aws_request_id
        function_name = context.function_name

        # Create item to write to DynamoDB
        item = {
            'id': DEFAULT_ID,
            'timestamp': timestamp,
            'writer_region': REGION,
            'request_id': request_id,
            'request_method': http_method,
            'request_path': path,
            'source_ip': source_ip,
            'function_name': function_name,
            #'event_data': json.dumps(event, default=str)
        }

        # Write the item to DynamoDB with the default ID
        response = table.put_item(Item=item)

        # Return a success response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'message': 'Data written to DynamoDB Global Table',
                'itemId': DEFAULT_ID,
                'timestamp': timestamp,
                'region': REGION,
                'requestId': request_id
            })
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'message': f'Error writing to DynamoDB: {str(e)}',
                'region': REGION,
                'requestId': context.aws_request_id if context else 'UNKNOWN'
            })
        }
