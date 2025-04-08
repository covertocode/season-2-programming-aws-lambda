import os
import boto3

def handler(event, context):
    environment = os.environ['ENVIRONMENT']
    parameter_name = os.environ['PARAMETER_NAME']

    # Create SSM client
    ssm = boto3.client('ssm')

    # Get parameter value
    try:
        response = ssm.get_parameter(Name=parameter_name, WithDecryption=False)
        resource_data = response['Parameter']['Value']
    except Exception as e:
        resource_data = "Error reading parameter"

    html_response = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Welcome - {environment}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                max-width: 800px;
                margin: 0 auto;
            }}
            h1, h2 {{
                color: #333;
                border-bottom: 1px solid #ccc;
            }}
            p {{
                margin-bottom: 16px;
            }}
            .resource-data {{
                background-color: #f5f5f5;
                padding: 10px;
                border-radius: 4px;
                margin: 20px 0;
            }}
        </style>
    </head>
    <body>
        <h1>Welcome!</h1>
        <h2>This is the <bold>{environment}</bold> environment.</h2>
        <div class="resource-data">
            <p><strong>Resource Data:</strong> {resource_data}</p>
        </div>
        <p>Get ready to learn more about CI/CD and several amazing tools that simplify testing, building, and deploying software.</p>
        <p>This welcome page is just the beginning. Take the next step by deploying the code for the application.</p>
    </body>
    </html>
    """
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html',
        },
        'body': html_response
    }
