all: build deploy

build:
	./build.sh

deploy:
	./deploy.sh

test:
	./test.sh

x-delete:
	@echo "WARNING: This will delete all resources and is IRREVERSIBLE."
	@read -p "Are you sure you want to continue? (yes/no): " confirm; \
	if [ "$$confirm" != "yes" ]; then \
		echo "Cleanup cancelled."; \
		exit 0; \
	fi
	./x-delete.sh
