# Chapter 5 Part 1: Deploy a Mutli-Function API

Application consists of an API with:

- An API Gateway for routing between functions
- A DynamoDB for data storage
- A function to write temperature data to the DB
- A function to query the DB by location

## Prerequisites

- AWS CLI installed and configured
- AWS SAM CLI installed
- Python 3.10 or later

## Installation

1. Install the AWS CLI and the AWS SAM CLI:

```bash
# macOS
brew install aws-sam-cli
```

1. Configure your AWS credentials:

```bash
aws configure
```

## Build and Deploy

```bash
sam build
sam deploy --guided
```

The `--guided` flag will walk you through the deployment process, asking for:

- Stack name
- AWS Region
- Confirm changes before deploy
- Allow SAM CLI IAM role creation
- Save arguments to configuration file

Sample responses to the `--guided` prompts:

```bash
 Setting default arguments for 'sam deploy'
 =========================================
 Stack Name [sam-app]: ch5-weather-api
 AWS Region [us-west-2]:
 Confirm changes before deploy [y/N]:
 Allow SAM CLI IAM role creation [Y/n]:
 Disable rollback [y/N]:
 WeatherEventLambda has no authentication. Is this okay? [y/N]: y
 WeatherQueryLambda has no authentication. Is this okay? [y/N]: y
 Save arguments to configuration file [Y/n]: Y
 SAM configuration file [samconfig.toml]:
 SAM configuration environment [default]:
```

## Use the Application

1. After deploying the application, get the URL from the CloudFormation stack's output and save it to an environment variable.

    ```bash
    export APP_URL="YOUR_URL_ENDPOINT"
    ```

1. Write data to the DB using `curl` and the API's `/events` route.

    ```bash
    curl -d '{"location_name":"Brooklyn, NY", "temperature":91, "timestamp":'"$(date +%s)"', "latitude": 40.70, "longitude": -73.99}' -H "Content-Type: application/json" -X POST "${APP_URL}/events"

    curl -d '{"location_name":"Oxford, UK", "temperature":64, "timestamp":'"$(date +%s)"', "latitude": 51.75, "longitude": -1.25}' -H "Content-Type: application/json" -X POST "${APP_URL}/events"
    ```

1. Read data from the DB using `curl` and the API's `/locations` route.

    ```bash
    curl "${APP_URL}/locations"
    ```

<!-- FooterStart -->
---
[← Chapter 4: Deploy Functions that use the Lambda Environment](../chapter-4-operating-aws-lambda-functions/README.md) | [Season 2: Programming AWS Lambda →](../README.md)
<!-- FooterEnd -->
