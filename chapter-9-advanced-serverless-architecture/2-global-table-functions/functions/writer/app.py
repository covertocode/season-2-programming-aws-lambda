import json
import boto3
import os
import uuid
from datetime import datetime

# Get environment variables
TABLE_NAME = os.environ['TABLE_NAME']
REGION = os.environ['REGION']

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name=REGION)
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    """
    Lambda function to write items to the DynamoDB Global Table.
    Expected event format:
    {
        "item_data": {
            "key1": "value1",
            "key2": "value2"
        }
    }
    """
    try:
        # Extract data from the event
        item_data = event.get('item_data', {})
        
        # Add required fields
        item = {
            'id': str(uuid.uuid4()),  # Generate a unique ID
            'timestamp': datetime.utcnow().isoformat(),
            'writer_region': REGION,
            **item_data
        }
        
        # Write the item to DynamoDB
        response = table.put_item(Item=item)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Item successfully written to DynamoDB',
                'item_id': item['id'],
                'region': REGION,
                'requestId': context.aws_request_id
            })
        }
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': f'Error writing to DynamoDB: {str(e)}',
                'region': REGION,
                'requestId': context.aws_request_id
            })
        }