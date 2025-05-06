import json
import uuid


def lambda_handler(event, context):
    # create a UUID for the request
    request_id = str(uuid.uuid4())
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"hello world from {request_id}",
        }),
    }


if __name__ == "__main__":
    # test the function locally
    event = {}
    context = {}
    print(lambda_handler(event, context))
