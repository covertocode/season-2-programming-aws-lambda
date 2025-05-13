#!/bin/bash

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Error: jq is not installed. Please install it using your package manager:"
    echo "  - For macOS: brew install jq"
    echo "  - For Ubuntu/Debian: sudo apt-get install jq"
    echo "  - For CentOS/RHEL: sudo yum install jq"
    exit 1
fi

WRITE_ENDPOINT=$(aws cloudformation describe-stacks --region=us-east-1 --query "Stacks[?StackName=='global-table-writer'][].Outputs[?OutputKey=='WriterFunctionUrl'].OutputValue" --output text)

echo "# $(date) Writing to the table..."
curl -s ${WRITE_ENDPOINT}

for region in us-east-2 us-west-1 us-west2;
do
    READ_ENDPOINT=$(aws cloudformation describe-stacks --region=${region} --query "Stacks[?StackName=='global-table-reader-${region}'][].Outputs[?OutputKey=='ReaderFunctionUrl'].OutputValue" --output text)

    echo "# $(date) ${region} Reading from the table..."
    curl -s ${READ_ENDPOINT} | jq
done
