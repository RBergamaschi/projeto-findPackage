.PHONY: build up down down-v logs logs-app logs-db restart shell ps rebuild

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

down-v:
	docker compose down -v

logs:
	docker compose logs -f

logs-app:
	docker compose logs -f app

logs-db:
	docker compose logs -f db

restart:
	docker compose restart

shell:
	docker compose exec app bash

ps:
	docker compose ps

rebuild:
	docker compose down
	docker compose up --build -d
