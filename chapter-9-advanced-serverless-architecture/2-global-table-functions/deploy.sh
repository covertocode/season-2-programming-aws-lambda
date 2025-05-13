#!/bin/bash
# Script to deploy Lambda functions across multiple regions
set -e

# Configuration
GLOBAL_TABLE_NAME="global-table-demo"  # Replace with your table name
WRITER_TEMPLATE="writer-template.yaml"
READER_TEMPLATE="reader-template.yaml"

# Deploy writer function to us-east-1
echo "# $(date) Deploying writer function to us-east-1..."
sam deploy \
  --template-file $WRITER_TEMPLATE \
  --stack-name global-table-writer \
  --region us-east-1 \
  --parameter-overrides \
    GlobalTableName=$GLOBAL_TABLE_NAME \
    FunctionNameSuffix="writer" \
  --capabilities CAPABILITY_IAM

# Deploy reader functions to their respective regions
echo "# $(date) Deploying reader function to us-east-2..."
sam deploy \
  --template-file $READER_TEMPLATE \
  --stack-name global-table-reader-east2 \
  --region us-east-2 \
  --parameter-overrides \
    GlobalTableName=$GLOBAL_TABLE_NAME \
    FunctionNameSuffix="reader" \
  --capabilities CAPABILITY_IAM

echo "# $(date) Deploying reader function to us-west-1..."
sam deploy \
  --template-file $READER_TEMPLATE \
  --stack-name global-table-reader-west1 \
  --region us-west-1 \
  --parameter-overrides \
    GlobalTableName=$GLOBAL_TABLE_NAME \
    FunctionNameSuffix="reader" \
  --capabilities CAPABILITY_IAM

echo "# $(date) Deploying reader function to us-west-2..."
sam deploy \
  --template-file $READER_TEMPLATE \
  --stack-name global-table-reader-west2 \
  --region us-west-2 \
  --parameter-overrides \
    GlobalTableName=$GLOBAL_TABLE_NAME \
    FunctionNameSuffix="reader" \
  --capabilities CAPABILITY_IAM

echo "# $(date) Deployment complete!"
