#!/bin/bash

# Exit on error
set -e

# Get current date for stack name
STACK_NAME="functional-test-$(date +%Y%m%d%H%M%S)"

echo "Starting functional test with stack name: $STACK_NAME"

# Step 1: Build and deploy the template
echo "Building and deploying the template..."
sam build
sam deploy --stack-name "$STACK_NAME" --capabilities CAPABILITY_IAM --no-fail-on-empty-changeset

# Step 2: Get stack outputs
echo "Getting stack outputs..."
API_ENDPOINT=$(aws cloudformation describe-stacks --query "Stacks[?StackName=='$STACK_NAME'][].Outputs[?OutputKey=='ApiEndpoint'].OutputValue" --output text)
export API_ENDPOINT

echo "API Endpoint: $API_ENDPOINT"

# Step 4: Run the create-weather-data.py script
echo "Writing test data to the API..."
python3 create-weather-data.py

# Step 5: Run the verification script
echo "Running verification script..."
python3 verify-weather-data.py
VERIFICATION_RESULT=$?

# Step 6: Clean up if tests passed
if [ $VERIFICATION_RESULT -eq 0 ]; then
    echo "Tests passed. Cleaning up stack..."
    sam delete --stack-name "$STACK_NAME" --no-prompts
else
    echo "Tests failed. Stack will be left in place for investigation."
    echo "Stack name: $STACK_NAME"
    exit 1
fi
