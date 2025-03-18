connect:
	aws ssm start-session --target=$(shell aws ec2 describe-instances --query 'Reservations[].Instances[].InstanceId' --filters "Name=instance-state-name,Values=running" "Name=tag:aws:cloudformation:logical-id,Values=JavaServer0" --output=text)
