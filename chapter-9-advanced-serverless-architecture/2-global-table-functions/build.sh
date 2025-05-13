#!/bin/bash
# Build script for SAM templates

# Ensure we're in the project root directory
echo "Building SAM templates..."

# Build the writer template
echo "Building writer template..."
sam build --template-file writer-template.yaml

# Build the reader template
echo "Building reader template..."
sam build --template-file reader-template.yaml

echo "Build complete! You can now deploy to multiple regions using the deploy script."