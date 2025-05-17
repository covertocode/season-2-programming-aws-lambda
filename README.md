# Season 2: Programming AWS Lambda

1. Use the CloudFormation template to create a server: [lab-server-cloudformation.yml](./lab-server-cloudformation.yml)
1. Connect to the server (Details coming soon!)
2. Use these steps to set up the environment:

   ```bash
   sudo yum install -y git
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

   # (copy and paste the shell configuration into shell-setup.sh)
   chmod +x ./shell-setup.sh
   ./shell-setup.sh
   which brew
   brew install awscli@1

   # (need details here on creating IAM account and credentials)
   aws configure
   aws sts get-caller-identity

   # For details on JAVA: https://docs.aws.amazon.com/corretto/
   sudo yum install java-23-amazon-corretto-devel
   sudo yum install java-21-amazon-corretto-devel

   # Select the java version you want to use (21, perhaps?)
   sudo update-alternatives --config java
   java -version

   # Install the SAM CLI and Maven
   brew install aws-sam-cli maven maven-completion
   ```

<!-- FooterStart -->
---
[Chapter 2: Hello World Java 21 →](chapter-2-getting-started-with-aws-lambda/README.md)
<!-- FooterEnd -->
