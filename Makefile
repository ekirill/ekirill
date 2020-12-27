prod-build:
	docker-compose -f ./docker-compose.yml -f ./docker-compose.prod.yml build

prod-up:
	docker-compose -f ./docker-compose.yml -f ./docker-compose.prod.yml up -d

prod-down:
	docker-compose -f ./docker-compose.yml -f ./docker-compose.prod.yml down

prod-logs:
	docker-compose -f ./docker-compose.yml -f ./docker-compose.prod.yml logs --tail=200 -f

dev-build:
	docker-compose -f ./docker-compose.yml -f ./docker-compose.dev.yml build

dev-up:
	docker-compose -f ./docker-compose.yml -f ./docker-compose.dev.yml up

dev-down:
	docker-compose -f ./docker-compose.yml -f ./docker-compose.dev.yml down

dev-logs:
	docker-compose -f ./docker-compose.yml -f ./docker-compose.dev.yml logs --tail=200 -f

dev-web-run: RUN=bash
dev-web-run:
	docker-compose -f ./docker-compose.yml -f ./docker-compose.dev.yml run --rm web $(RUN)

dev-front:
	docker-compose -f ./docker-compose.yml -f ./docker-compose.dev.yml up nginx
