all: requirements test

requirements:
	pip install -q -U pip
	pip install -q -r requirements.txt

test:
	LOCATIONS_TABLE=testing python -m unittest -v tests/test_weather_lambdas.py
