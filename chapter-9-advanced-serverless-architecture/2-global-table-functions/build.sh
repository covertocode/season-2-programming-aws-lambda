#!/bin/bash
# Build script for SAM templates
set -e

# Build the writer template
echo "# $(date) Building writer template..."
sam build --template-file writer-template.yaml

# Build the reader template
echo "# $(date) Building reader template..."
sam build --template-file reader-template.yaml
