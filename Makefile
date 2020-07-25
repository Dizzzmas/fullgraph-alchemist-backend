.PHONY: idb seed flask-init-db run

# init DB
init-db: idb
idb: dropcreatedb flask-init-db seed

flask-init-db:
	flask db upgrade

dropcreatedb:
	dropdb fullgraph_alchemist --if-exists
	createdb fullgraph_alchemist

seed:
	$(PYTHON) flask seed

run:
	FLASK_ENV=development flask run --reload --without-threads