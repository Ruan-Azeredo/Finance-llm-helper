install:
	@pip install -r requirements.txt

test:
	@cd src && pytest -m "not llm and not db"

init_db:
	@cd src && POSTGRES_HOST=localhost python initialize_db.py

start:
	@cd src && POSTGRES_HOST=localhost uvicorn server:app --host 0.0.0.0 --port 8000

devstart:
	@set POSTGRES_HOST=localhost && cd src && uvicorn server:app --host 0.0.0.0 --port 8000 --reload

migrate:
	@cd src && PYTHONPATH=./ python database/migrations/$(file).py

build: install init_db start

#run: make build
