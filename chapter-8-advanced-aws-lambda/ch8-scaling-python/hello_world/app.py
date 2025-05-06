"""
This is a hello world Lambda function for demonstrating Lambda scaling.
"""

import json
import time
import uuid


def lambda_handler(event, context):
    """
    Lambda function handler.
    """
    # create a UUID for the request
    request_id = str(uuid.uuid4())

    # sleep for 5 seconds
    time.sleep(2)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "ID": f"Python {request_id[-2:]}",
            }
        ),
    }


if __name__ == "__main__":
    # test the function locally
    event = {}
    context = {}
    print(lambda_handler(event, context))
