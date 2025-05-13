import json
import boto3
import os
import datetime

# Get environment variables
TABLE_NAME = os.environ['TABLE_NAME']
REGION = os.environ['REGION']
DEFAULT_ID = os.environ.get('DEFAULT_ID', 'default-item-id')

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name=REGION)
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    """
    Lambda function that reads the default item from the DynamoDB Global Table.
    Returns the data as JSON.
    """
    try:
        # Get the default item from DynamoDB
        response = table.get_item(Key={'id': DEFAULT_ID})
        
        # Extract the item if it exists
        item = response.get('Item', {})
        
        if not item:
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'message': f'Item with ID {DEFAULT_ID} not found',
                    'region': REGION,
                    'timestamp': datetime.datetime.utcnow().isoformat(),
                    'requestId': context.aws_request_id
                })
            }
        
        # Add some metadata about the read operation
        result = {
            'data': item,
            'metadata': {
                'reader_region': REGION,
                'read_timestamp': datetime.datetime.utcnow().isoformat(),
                'function_name': context.function_name,
                'request_id': context.aws_request_id
            }
        }
        
        # Return the item data as JSON
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(result, default=str)
        }
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'message': f'Error reading from DynamoDB: {str(e)}',
                'region': REGION,
                'requestId': context.aws_request_id if context else 'UNKNOWN'
            })
        }