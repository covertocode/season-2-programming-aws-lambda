from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools import Logger
from aws_lambda_powertools import Tracer
from aws_lambda_powertools import Metrics
from aws_lambda_powertools.metrics import MetricUnit
import json

app = APIGatewayRestResolver()
tracer = Tracer()
logger = Logger()
metrics = Metrics(namespace="Chapter8")

@app.get("/hello")
@tracer.capture_method
def hello():
    # adding custom metrics
    metrics.add_metric(name="PythonHelloWorldInvocations", unit=MetricUnit.Count, value=1)

    try:
        # Randomly inject an error
        import random
        if random.choice([True, False]):
            raise Exception("Error mode selected")

        logger.info("Hello world API - HTTP 200")
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Request processed successfully."})
        }
    except Exception as e:
        logger.error(f"Hello world API - HTTP 500: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Internal Server Error: {str(e)}"})
        }

# Enrich logging with contextual information from Lambda
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
# Adding tracer
# See: https://awslabs.github.io/aws-lambda-powertools-python/latest/core/tracer/
@tracer.capture_lambda_handler
# ensures metrics are flushed upon request completion/failure and capturing ColdStart metric
@metrics.log_metrics(capture_cold_start_metric=True)
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
