lint:
	pipenv run tox -e lint
.PHONY: lint

type-check:
	pipenv run tox -e type-check
.PHONY: type-check

test:
	pipenv run tox -e unit
.PHONY: test

start-api:
	docker compose run api
.PHONY: start-api

clean-docker:
	docker system prune -f
	docker images | grep 'watchlist-recommender-api' | awk '{print $$3}' | xargs docker rmi
.PHONY: clean-docker