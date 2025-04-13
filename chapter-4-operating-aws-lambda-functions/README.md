# Chapter 4: Deploy Functions that use the Lambda Environment

This is a simple AWS SAM application that creates two Lambda functions (staging and production) with function URLs.  The functions interact with the Lambda Runtime Environment and AWS resources by:

- Reading ENVIRONMENT_VARIABLES from AWS Lambda to use as parameters
- Using the value of the parameters to access AWS Parameter Store
- Reporting the parameter values in HTML output

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

2. Configure your AWS credentials:

```bash
aws configure
```

## Build and Deploy

To build and deploy the application:

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

Sample responses to the `--guided` prompts:

```bash
 Setting default arguments for 'sam deploy'
 =========================================
 Stack Name [sam-app]: python-ssm-parameters-v2
 AWS Region [us-west-2]:
 Confirm changes before deploy [y/N]:
 Allow SAM CLI IAM role creation [Y/n]:
 Disable rollback [y/N]: y
 StagingFunction Function Url has no authentication. Is this okay? [y/N]: y
 ProductionFunction Function Url has no authentication. Is this okay? [y/N]: y
 Save arguments to configuration file [Y/n]:
 SAM configuration file [samconfig.toml]:
 SAM configuration environment [default]:
```

If you make changes to the code, you can redeploy with:

```
sam build
sam deploy
```

## Accessing the Function URLs

After deployment, you can find the function URLs in the CloudFormation stack outputs:

- StagingFunctionUrl
- ProductionFunctionUrl

## Cleanup

To delete the application and all its resources:

```bash
sam delete
```

<!-- FooterStart -->
---
[← hello-world-java21](../chapter-2-getting-started-with-aws-lambda/README.md) | [Chapter 5: Deploy a Mutli-Function API →](../chapter-5-api/README.md)
<!-- FooterEnd -->
