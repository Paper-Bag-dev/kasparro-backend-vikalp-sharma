up:
	docker-compose up -d --build

down:
	docker-compose down

logs:
	docker-compose logs -f api

ps:
	docker-compose ps

test:
	docker-compose run --rm api pytest -q
