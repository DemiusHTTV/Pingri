PHONY: up down

up:
	@echo "Starting containers..."
	docker compose up -d
	@echo "Containers started."

down:
	@echo "Stopping containers..."
	docker compose down -v
	@echo "Containers stopped."

