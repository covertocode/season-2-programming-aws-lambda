# Multi-Region SAM Deployment Guide

This guide will help you set up and deploy SAM applications to multiple AWS regions.

## Understanding the Error

The error message:
```
Error: Stack aws-sam-cli-managed-default is missing Tags and/or Outputs information and therefore not in a healthy state (Current state:REVIEW_IN_PROGRESS). Failing as the stack was likely not created by the AWS SAM CLI
```

This occurs because:
- SAM CLI creates a managed CloudFormation stack in each region to store deployment artifacts
- You've only set up this stack in us-west-2, but are trying to deploy to other regions
- Each region needs its own "bootstrap" stack before deployment

## Step 1: Bootstrapping All Required Regions

### Option 1: Using the bootstrap script

1. Save the provided bootstrap script
2. Make it executable: `chmod +x bootstrap-script.sh`
3. Run it: `./bootstrap-script.sh`

### Option 2: Manual bootstrap

Run the bootstrap command manually for each region:

```bash
# Bootstrap us-east-1 (writer region)
sam bootstrap --region us-east-1 --no-interactive

# Bootstrap other reader regions
sam bootstrap --region us-east-2 --no-interactive
sam bootstrap --region us-west-1 --no-interactive
# (us-west-2 is already set up)
```

## Step 2: Build Your SAM Templates (Once)

After bootstrapping all regions, build your templates:

```bash
sam build --template-file writer-template.yaml
sam build --template-file reader-template.yaml
```

## Step 3: Deploy to Each Region

Now deploy to each bootstrapped region:

```bash
# Deploy writer to us-east-1
sam deploy --template-file writer-template.yaml \
  --stack-name global-table-writer \
  --region us-east-1 \
  --parameter-overrides GlobalTableName=my-global-table \
  --capabilities CAPABILITY_IAM

# Deploy readers to other regions
sam deploy --template-file reader-template.yaml \
  --stack-name global-table-reader-east2 \
  --region us-east-2 \
  --parameter-overrides GlobalTableName=my-global-table \
  --capabilities CAPABILITY_IAM

# Repeat for other regions
```

## Additional Notes

1. **S3 Buckets**:
   - The bootstrap process creates an S3 bucket in each region to store deployment artifacts
   - Format: `aws-sam-cli-managed-default-samclisourcebucket-<hash>`

2. **One-time Setup**:
   - Bootstrapping only needs to be done once per region
   - Future deployments can reuse the same bootstrap resources

3. **AWS Credentials**:
   - Ensure your AWS credentials have permissions in all target regions
   - If using profiles, specify with `--profile` in the commands

4. **Clean Up**:
   - When no longer needed, you can remove the bootstrap resources:
   ```bash
   sam delete --stack-name aws-sam-cli-managed-default --region <region-name>
   ```

5. **Troubleshooting Failed Bootstrap**:
   - If a bootstrap attempt fails, go to the CloudFormation console in that region
   - Delete any failed `aws-sam-cli-managed-default` stack
   - Try the bootstrap command again