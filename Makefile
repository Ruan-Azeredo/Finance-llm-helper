OS := $(shell uname)

install:
	@pip install -r requirements.txt

test:
	@cd src && pytest -m "not llm and not db"

init_db:
ifeq ($(OS), Linux)
	@cd src && POSTGRES_HOST=0.0.0.0 python initialize_db.py
else ifeq ($(OS), Darwin)
	@cd src && POSTGRES_HOST=0.0.0.0 python initialize_db.py
else
	@set POSTGRES_HOST=0.0.0.0 && cd src && python initialize_db.py
endif

start:
ifeq ($(OS), Linux)
	@cd src && POSTGRES_HOST=0.0.0.0 uvicorn server:app --host 0.0.0.0 --port 8000
else ifeq ($(OS), Darwin)
	@cd src && POSTGRES_HOST=0.0.0.0 uvicorn server:app --host 0.0.0.0 --port 8000
else
	@set POSTGRES_HOST=0.0.0.0 && cd src && uvicorn server:app --host 0.0.0.0 --port 8000
endif

devstart:
ifeq ($(OS), Linux)
	@cd src && POSTGRES_HOST=0.0.0.0 uvicorn server:app --host 0.0.0.0 --port 8000 --reload
else ifeq ($(OS), Darwin)
	@cd src && POSTGRES_HOST=0.0.0.0 uvicorn server:app --host 0.0.0.0 --port 8000 --reload
else
	@set POSTGRES_HOST=0.0.0.0 && cd src && uvicorn server:app --host 0.0.0.0 --port 8000 --reload
endif

# make script file=script_name
script:
ifeq ($(OS), Linux)
	@cd src && POSTGRES_HOST=0.0.0.0 PYTHONPATH=./ python scripts/$(file).py
else ifeq ($(OS), Darwin)
	@cd src && POSTGRES_HOST=0.0.0.0 PYTHONPATH=./ python scripts/$(file).py
else
	@set POSTGRES_HOST=0.0.0.0 && cd src && set PYTHONPATH=./ && python scripts/$(file).py
endif


build: install init_db start

#run: make build
