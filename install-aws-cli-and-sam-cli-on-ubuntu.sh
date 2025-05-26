#!/bin/bash
apt install curl maven unzip wget zip jq nodejs npm -y
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
wget "https://github.com/aws/aws-sam-cli/releases/latest/download/aws-sam-cli-linux-x86_64.zip"
unzip awscliv2.zip
unzip aws-sam-cli-linux-x86_64.zip -d sam
./aws/install
./sam/install
/usr/local/bin/sam --version
/usr/local/bin/aws --version
