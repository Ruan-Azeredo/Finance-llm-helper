install:
	@pip install -r requirements.txt

init_db:
	@python src/initialize_db.py

start:
	@cd src && uvicorn src.server:app --host 0.0.0.0 --port 8000

build: install init_db start

#run: make build

# still not finished