#!/bin/bash

STACK_NAME="ch8-scaling-java"

API_ENDPOINT=$(aws cloudformation describe-stacks --query "Stacks[?StackName=='$STACK_NAME'][].Outputs[?OutputKey=='ApiEndpoint'].OutputValue" --output text)

while :;
do
    echo "$(date +%T) $(curl -s ${API_ENDPOINT})";
done
