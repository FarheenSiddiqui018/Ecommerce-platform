# Makefile

.PHONY: build up down test format pre-commit shell migrate logs

# Define service names for easy reference
SERVICE_WEB=web
SERVICE_TEST=test

# Build all Docker images
build:
	docker-compose build

# Start all Docker containers in detached mode
up:
	docker-compose up -d

# Stop and remove all Docker containers
down:
	docker-compose down

# Run tests using the 'test' service
test:
	docker-compose run --rm $(SERVICE_TEST) pytest

# Format code using Black within the 'web' service
format:
	docker-compose run --rm $(SERVICE_WEB) black .

# Stream logs from all running Docker containers
logs:
	docker-compose logs -f

# Apply Alembic migrations within the 'web' service
migrate:
	docker-compose run --rm $(SERVICE_WEB) alembic upgrade head

# Open a shell inside the 'web' service container
shell:
	docker-compose run --rm $(SERVICE_WEB) sh
