DOCKER_COMPOSE_FILE=docker-compose.yaml
APP_CONTAINER_NAME=fin_info_app

status:
	docker ps -a && docker images

build:
	docker rmi -f fin_info && docker-compose -f ${DOCKER_COMPOSE_FILE} build

start:
	docker-compose -f ${DOCKER_COMPOSE_FILE} up -d

logs:
	docker-compose logs --tail 200

shell:
	docker exec -it ${APP_CONTAINER_NAME} bash

migrations:
	docker-compose  run --rm --entrypoint "python3.12 manage.py makemigrations" app

migrate:
	docker-compose  run --rm --entrypoint "python3.12 manage.py migrate --no-input" app

static:
	docker-compose  run --rm --entrypoint "python3.12 manage.py collectstatic --no-input" app

createsuperuser:
	docker-compose  run --rm --entrypoint "python3.12 manage.py createsuperuser " app

translate:
	docker-compose  run --rm --entrypoint "python3.12 manage.py compilemessages --use-fuzzy " app

unit-tests:
	docker-compose  run --rm --entrypoint "python3.12 manage.py test tests.unit" app

integration-tests:
	docker-compose  run --rm --entrypoint "python3.12 manage.py test tests.integration" app

all-tests:
	docker-compose  run --rm --entrypoint "python3.12 manage.py test tests" app

coverage-tests:
	docker-compose  run --rm --entrypoint "coverage run --source='.' manage.py test tests; coverage report" app

coverage-report:
	docker-compose  run --rm --entrypoint 'coverage report --omit="tests/*,__init__.py,media/*,static/*,*/migrations/*,config/*"' app
