#!/bin/bash

VERIFICATION_RESULT=1

# Define the final statement as a function
final_statement() {
    # Step 6: Clean up if tests passed
    if [ $VERIFICATION_RESULT -eq 0 ]; then
        echo "# $(date) Tests passed. Cleaning up stack..."
        sam delete --stack-name "$STACK_NAME" --no-prompts
    else
        echo "# $(date) Tests failed. $STACK_NAME will be left in place for investigation."
        echo "# $(date) After debugging, delete it with this command:"
        echo "# $(date) sam delete --stack-name "$STACK_NAME" --no-prompts"
        exit 1
    fi
}

# Step 0: Set up the test environment
# Set the trap to execute the final statement on EXIT
trap final_statement EXIT

# Get current date for stack name
STACK_NAME="end-to-end-test-$(date +%Y%m%d%H%M%S)"

echo "# $(date) Starting end-to-end test with stack name: $STACK_NAME"

echo
echo
echo "# $(date) Install requirements"
make development-requirements

# Step 1: Build and deploy the template
echo
echo
echo "# $(date) Building and deploying the template..."
sam build
sam deploy --stack-name "$STACK_NAME" \
    --capabilities CAPABILITY_IAM \
    --no-confirm-changeset \
    --disable-rollback

# Step 2: Get stack outputs
echo
echo
echo "# $(date) Getting stack outputs..."
API_ENDPOINT=$(aws cloudformation describe-stacks --query "Stacks[?StackName=='$STACK_NAME'][].Outputs[?OutputKey=='ApiEndpoint'].OutputValue" --output text)

export API_ENDPOINT

echo "# $(date) API Endpoint: $API_ENDPOINT"

# Step 3: Run the create-weather-data.py script
echo
echo
echo "# $(date) Writing test data to the API..."
python3 create-weather-data.py
CREATE_WEATHER_DATA_RESULT=$?
if [ $CREATE_WEATHER_DATA_RESULT -ne 0 ]; then
    echo "# $(date) Error writing test data to the API. Exiting..."
    exit 1
fi

# Step 4: Run the verification script
echo
echo
echo "# $(date) Running verification script..."
python3 verify-weather-data.py
VERIFICATION_RESULT=$?
if [ $VERIFICATION_RESULT -ne 0 ]; then
    echo "# $(date) Verification failed. Exiting..."
    exit 1
fi
