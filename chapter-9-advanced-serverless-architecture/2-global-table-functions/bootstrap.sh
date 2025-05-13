#!/bin/bash
# Script to bootstrap SAM CLI in multiple regions
set -e

# List of regions where you want to deploy
REGIONS=(
  "us-east-1"  # Writer region
  "us-east-2"  # Reader region
  "us-west-1"  # Reader region
  "us-west-2"  # Reader region (you already have this set up)
)

# Bootstrap each region
for region in "${REGIONS[@]}"; do
  echo "# $(date) Bootstrapping region: $region"

  # Run bootstrap command for the region
  sam bootstrap \
    --region "$region" \
    --no-interactive

  echo "# $(date) Completed bootstrapping for $region"
  echo "---------------------------------"
done

echo "# $(date) All regions have been bootstrapped for SAM CLI!"
