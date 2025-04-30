TARGETS = all requirements test

$(TARGETS):
	$(MAKE) -C src $@

development-requirements:
	pip install -q -U pip
	pip install -q --requirement development-requirements.txt

lint:
	sam validate --lint
	python3 -m flake8 --ignore=E501,E231 *.py
	python3 -m pylint --errors-only --disable=C0301 *.py
	python3 -m black --diff .
	python3 -m isort --diff .

fmt:
	python3 -m black .
	python3 -m isort .
build:
	sam build

deploy:
	sam deploy --no-confirm-changeset

create-weather-data:
	python3 ./create-weather-data.py

verify-weather-data:
	python3 ./verify-weather-data.py

functional-test:
	./functional-test.sh

outputs:
	@echo "SAM CLI outputs:"
	sam list stack-outputs --stack-name=chapter-6-and-7-testing-logging

	@echo "CloudFormation outputs:"
	aws cloudformation describe-stacks \
		--stack-name chapter-6-and-7-testing-logging \
		--query "Stacks[].Outputs" \
		--output=json

logs:
	sam logs --stack-name chapter-6-and-7-testing-logging

stacks:
	aws cloudformation describe-stacks \
		--query "Stacks[].{Name:StackName,Status:StackStatus}" \
		--output=table
