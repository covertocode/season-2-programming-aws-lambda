all: build deploy

build:
	sam build

deploy:
	sam deploy

x-delete:
	@echo "WARNING: This will delete all resources and is IRREVERSIBLE."
	@read -p "Are you sure you want to continue? (yes/no): " confirm; \
	if [ "$$confirm" != "yes" ]; then \
		echo "Cleanup cancelled."; \
		exit 0; \
	fi
	sam delete --no-prompts
