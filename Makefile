# Makes a local development environment
model_dev:
	docker-compose -f docker/docker-compose.yml build && \
	docker-compose -f docker/docker-compose.yml run --service-ports --rm model-development


