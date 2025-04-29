TARGETS = all requirements test

$(TARGETS):
	$(MAKE) -C src $@

build:
	sam build

deploy:
	sam deploy --no-confirm-changeset
