# AWS SAM Application

This is a simple AWS SAM application that creates two Lambda functions (staging and production) with function URLs.

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

## Deployment

To deploy the application:

```bash
# Build the application
sam build

# Deploy the application
sam deploy --guided --capabilities CAPABILITY_NAMED_IAM
```

The `--guided` flag will walk you through the deployment process, asking for:

- Stack name
- AWS Region
- Confirm changes before deploy
- Allow SAM CLI IAM role creation
- Save arguments to configuration file

Sample responses to the `--guided` prompts:

```
	Setting default arguments for 'sam deploy'
	=========================================
	Stack Name [sam-app]: python-ssm-parameters-v2
	AWS Region [us-west-2]:
	#Shows you resources changes to be deployed and require a 'Y' to initiate deploy
	Confirm changes before deploy [y/N]:
	#SAM needs permission to be able to create roles to connect to the resources in your template
	Allow SAM CLI IAM role creation [Y/n]:
	#Preserves the state of previously provisioned resources when an operation fails
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
