ci: build lint mypy run-test

build:
	sudo docker-compose --env-file=config/.env up -d

lint:
	sudo docker-compose exec -T web poetry run flake8 .

mypy:
	sudo docker-compose exec -T web poetry run mypy .

run-test:
	sudo docker-compose exec -T web poetry run pytest .
