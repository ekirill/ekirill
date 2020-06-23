build:
	docker-compose -f ./docker-compose.yml -f ./docker-compose.prod.yml build

up:
	docker-compose -f ./docker-compose.yml -f ./docker-compose.prod.yml up -d

down:
	docker-compose -f ./docker-compose.yml -f ./docker-compose.prod.yml down

logs:
	docker-compose -f ./docker-compose.yml -f ./docker-compose.prod.yml logs -f
