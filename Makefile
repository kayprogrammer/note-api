ifneq (,$(wildcard ./.env))
include .env
export 
ENV_FILE_PARAM = --env-file .env

endif

build:
	docker-compose up --build -d --remove-orphans

up:
	docker-compose up -d

down:
	docker-compose down

show-logs:
	docker-compose logs

serv:
	python manage.py runserver

mmig:
	python manage.py makemigrations
mig:
	python manage.py migrate
shell:
	python manage.py shell
requirements:
	pip install -r requirements.txt
