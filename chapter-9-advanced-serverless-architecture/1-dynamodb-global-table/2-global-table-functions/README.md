# Deployment Guide for Lambda Functions with DynamoDB Global Table

This guide provides instructions for deploying Lambda functions across different regions that work with your existing DynamoDB Global Table.

## Prerequisites

1. An AWS account with CLI access configured
2. AWS SAM CLI installed (https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
3. The DynamoDB Global Table (`global-table-demo`) already deployed
4. Python 3.9+ installed

## Project Structure

Create the following directory structure:

```
.
├── template.yaml           # SAM template
├── functions
│   ├── writer
│   │   └── app.py          # Writer Lambda function code
│   └── reader
│       └── app.py          # Reader Lambda function code
```

## Deployment Steps

1. **Create Function Directories**

   ```bash
   mkdir -p functions/writer functions/reader
   ```

2. **Copy the Lambda Function Code**

   Copy the writer function code to `functions/writer/app.py` and the reader function code to `functions/reader/app.py`

3. **Deploy with SAM**

   ```bash
   sam build
   sam deploy --guided
   ```

   During guided deployment, you'll be prompted for:
   - Stack name (e.g., `lambda-global-table-stack`)
   - AWS Region (deploy to `us-east-1` first)
   - Parameters:
     - `GlobalTableName`: Enter your Global Table name (default: `global-table-demo`)
   - Confirm changes and deploy

4. **Testing**

   Test the Writer Lambda function (us-east-1):
   ```json
   {
     "item_data": {
       "message": "Hello from us-east-1",
       "timestamp_local": "2025-05-13T10:00:00"
     }
   }
   ```

   Test a Reader Lambda function (any other region):
   ```json
   {
     "operation": "scan",
     "limit": 10
   }
   ```

   or to get a specific item:
   ```json
   {
     "operation": "get",
     "id": "[ID_FROM_WRITER_RESPONSE]"
   }
   ```

## Important Notes

1. **Regional Deployment**
   While the template includes all Lambda functions, each function should ideally be deployed in its specific region. For a production setup, consider creating separate regional templates.

2. **Cross-Region IAM Roles**
   This template uses a single IAM role for simplicity. In a production environment, you might want to create region-specific roles.

3. **Lambda Environment Variables**
   Each Lambda knows which region it should connect to through the `REGION` environment variable.

4. **Replication Latency**
   DynamoDB Global Tables typically have replication latency under 1 second, but allow for potential delays when reading immediately after writing.

5. **Cost Optimization**
   The template uses minimal settings. For production, optimize memory, timeout, and consider using provisioned concurrency if needed.

6. **Monitoring**
   Consider adding CloudWatch Alarms and X-Ray tracing for production monitoring.
