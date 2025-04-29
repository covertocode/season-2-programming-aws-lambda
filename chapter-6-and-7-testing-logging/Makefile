TARGETS = all requirements test

$(TARGETS):
	$(MAKE) -C src $@

development-requirements:
	pip install -U pip
	pip install --requirement development-requirements.txt

lint:
	sam validate --lint

build:
	sam build

deploy:
	sam deploy --no-confirm-changeset
