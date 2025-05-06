#!/bin/bash

STACK_NAME="ch8-scaling-java-sleep"

API_ENDPOINT=$(aws cloudformation describe-stacks --query "Stacks[?StackName=='$STACK_NAME'][].Outputs[?OutputKey==    'ApiEndpoint'].OutputValue" --output text)

while :;
do
    echo "$(date) $(curl -s ${API_ENDPOINT})";
done
