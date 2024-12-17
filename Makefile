install:
	@pip install -r requirements.txt

test:
	@cd src && pytest -m "not llm"

init_db:
	@cd src && python initialize_db.py

start:
	@cd src && uvicorn server:app --host 0.0.0.0 --port 8000

devstart:
	@cd src && uvicorn server:app --host 0.0.0.0 --port 8000 --reload

migrate:
	@cd src && PYTHONPATH=./ python database/migrations/$(file).py

build: install init_db start

#run: make build
