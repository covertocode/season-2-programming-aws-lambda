# SAM Multi-Region Build and Deploy Guide

This guide explains how to build and deploy Lambda functions to work with your DynamoDB Global Table across multiple regions.

## Project Structure

Before building, ensure your project has this structure:

```
project-root/
├── writer-template.yaml        # SAM template for the writer function
├── reader-template.yaml        # SAM template for the reader functions
├── functions/
│   ├── writer/
│   │   └── app.py              # Writer Lambda code
│   └── reader/
│       └── app.py              # Reader Lambda code
├── build.sh                    # Optional build script
└── deploy.sh                   # Optional deployment script
```

## Build Process

### Option 1: Using the terminal directly

```bash
# Navigate to your project root
cd your-project-directory

# Build both templates
sam build --template-file writer-template.yaml
sam build --template-file reader-template.yaml
```

### Option 2: Using the build script

```bash
# Make the script executable
chmod +x build.sh

# Run the build script
./build.sh
```

## What happens during `sam build`

The `sam build` command:

1. Creates a `.aws-sam` directory in your project root
2. Resolves dependencies for your Lambda functions
3. Copies your code and dependencies into the build directory
4. Prepares the package for deployment

For Python functions, SAM will:
- Create a virtual environment
- Install dependencies from requirements.txt (if present)
- Package the code and dependencies

## Important Notes About Multi-Region Builds

1. **Build Once, Deploy Many**: 
   - You only need to build once, even when deploying to multiple regions
   - The same build artifacts can be deployed to any region

2. **Template Parameters**:
   - The templates use `!Ref AWS::Region` to get the deployment region
   - This ensures each function connects to the proper regional DynamoDB endpoint

3. **Requirements File** (Optional):
   If your functions have dependencies, add a requirements.txt file:
   ```
   # functions/writer/requirements.txt or functions/reader/requirements.txt
   boto3==1.26.0
   ```

4. **Next Steps**:
   After building, use the deploy script or manual commands to deploy to each region:
   ```bash
   # Example for one region
   sam deploy --template-file writer-template.yaml --stack-name global-table-writer --region us-east-1 --parameter-overrides GlobalTableName=my-global-table --capabilities CAPABILITY_IAM
   ```

## Troubleshooting

- If you get errors about missing modules, check that your build completed successfully
- Look in `.aws-sam/build` to confirm your code and dependencies were packaged correctly
- For permission errors, make sure you have the necessary AWS credentials configured