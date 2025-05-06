#!/bin/bash

# Set the PWD basename as the stack name
STACK_NAME=$(basename "$PWD")

API_ENDPOINT=$(aws cloudformation describe-stacks --query "Stacks[?StackName=='$STACK_NAME'][].Outputs[?OutputKey=='ApiEndpoint'].OutputValue" --output text)

while :;
do
    echo "$(date +%T) $(curl -s ${API_ENDPOINT})";
done
