.PHONY: up down logs ps

up:
	@echo "Starting containers..."
	docker compose up -d
	@echo "Containers started."

down:
	@echo "Stopping containers..."
	docker compose down
	@echo "Containers stopped."

logs:
	docker compose logs -f

ps:
	docker compose ps
