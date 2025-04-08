# AWS SAM Application

This is a simple AWS SAM application that creates two Lambda functions (staging and production) with function URLs.

## Prerequisites

- AWS CLI installed and configured
- AWS SAM CLI installed
- Python 3.10 or later

## Installation

1. Install the AWS SAM CLI:

```bash
brew install aws-sam-cli
```

2. Configure your AWS credentials:

```bash
aws configure
```

## Deployment

To deploy the application:

```bash
# Build the application
sam build

# Deploy the application
sam deploy --guided
```

The `--guided` flag will walk you through the deployment process, asking for:

- Stack name
- AWS Region
- Confirm changes before deploy
- Allow SAM CLI IAM role creation
- Save arguments to configuration file

## Testing Locally

You can test the application locally using:

```bash
sam local invoke StagingFunction
sam local invoke ProductionFunction
```

## Accessing the Function URLs

After deployment, you can find the function URLs in the CloudFormation stack outputs:

- Staging URL
- Production URL

## Cleanup

To delete the application and all its resources:

```bash
sam delete
```
