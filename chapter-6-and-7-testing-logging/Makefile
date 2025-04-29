TARGETS = all requirements test

$(TARGETS):
	$(MAKE) -C src $@

development-requirements:
	pip install -U pip
	pip install --requirement development-requirements.txt

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

weather-data:
	python3 ./create-weather-data.py
