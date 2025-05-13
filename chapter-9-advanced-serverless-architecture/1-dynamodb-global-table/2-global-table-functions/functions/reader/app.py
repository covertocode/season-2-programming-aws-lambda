import json
import boto3
import os

# Get environment variables
TABLE_NAME = os.environ['TABLE_NAME']
REGION = os.environ['REGION']

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name=REGION)
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    """
    Lambda function to read items from the DynamoDB Global Table.
    Supported operations:
    1. Get item by ID:
       { "operation": "get", "id": "some-uuid" }
    
    2. Scan table (with optional limit):
       { "operation": "scan", "limit": 10 }
    
    3. Query by attribute (if indexed):
       { "operation": "query", "attr_name": "some_attribute", "attr_value": "some_value" }
    """
    try:
        operation = event.get('operation', 'scan')
        
        if operation == 'get':
            # Get a specific item by ID
            item_id = event.get('id')
            if not item_id:
                return {
                    'statusCode': 400,
                    'body': json.dumps({
                        'message': 'Missing required parameter: id',
                        'region': REGION
                    })
                }
            
            response = table.get_item(Key={'id': item_id})
            item = response.get('Item', {})
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Item retrieved successfully' if item else 'Item not found',
                    'item': item,
                    'region': REGION,
                    'requestId': context.aws_request_id
                }, default=str)  # default=str handles datetime serialization
            }
            
        elif operation == 'scan':
            # Scan the table (with optional limit)
            limit = event.get('limit', 20)  # Default limit of 20 items
            
            response = table.scan(Limit=limit)
            items = response.get('Items', [])
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': f'{len(items)} items retrieved',
                    'count': len(items),
                    'items': items,
                    'region': REGION,
                    'requestId': context.aws_request_id
                }, default=str)
            }
            
        elif operation == 'query':
            # This is a simple implementation that would need to be enhanced
            # for production use with actual indexes
            return {
                'statusCode': 501,
                'body': json.dumps({
                    'message': 'Query operation not implemented in this example',
                    'region': REGION,
                    'requestId': context.aws_request_id
                })
            }
            
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'message': f'Invalid operation: {operation}',
                    'region': REGION,
                    'requestId': context.aws_request_id
                })
            }
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': f'Error reading from DynamoDB: {str(e)}',
                'region': REGION,
                'requestId': context.aws_request_id
            })
        }