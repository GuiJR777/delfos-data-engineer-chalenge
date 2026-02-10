VENV ?= .venv

PYTHON := python
PIP := pip

ifeq ($(OS),Windows_NT)
SHELL := cmd.exe
VENV_BIN := $(VENV)/Scripts
VENV_BIN_WIN := $(VENV)\\Scripts
ifneq ($(wildcard $(VENV_BIN)/python.exe),)
PYTHON := $(VENV_BIN_WIN)\\python.exe
PIP := $(VENV_BIN_WIN)\\pip.exe
else ifneq ($(wildcard venv/Scripts/python.exe),)
VENV := venv
VENV_BIN := $(VENV)/Scripts
VENV_BIN_WIN := $(VENV)\\Scripts
PYTHON := $(VENV_BIN_WIN)\\python.exe
PIP := $(VENV_BIN_WIN)\\pip.exe
endif
PYTHONPATH_CMD := set PYTHONPATH=src&&
else
SHELL := /bin/sh
VENV_BIN := $(VENV)/bin
ifneq ($(wildcard $(VENV_BIN)/python),)
PYTHON := $(VENV_BIN)/python
PIP := $(VENV_BIN)/pip
endif
PYTHONPATH_CMD := PYTHONPATH=src
endif

COMPOSE ?= docker compose
COMPOSE_FILE ?= docker/docker-compose.yml

DAGSTER ?= dagster
DAGSTER_FILE ?= src/orchestration/definitions.py

DATE ?=
SEED_ARGS ?=

.PHONY: setup seed up down reset logs ps health api etl dagster test

setup:
	python -m venv $(VENV)
	$(PYTHON) -m pip install -U pip
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m pip install -r requirements-dev.txt

seed:
	$(PYTHON) scripts/seed_source_db.py $(SEED_ARGS)

up:
	$(COMPOSE) -f $(COMPOSE_FILE) up -d

down:
	$(COMPOSE) -f $(COMPOSE_FILE) down

reset:
	$(COMPOSE) -f $(COMPOSE_FILE) down -v --remove-orphans

logs:
	$(COMPOSE) -f $(COMPOSE_FILE) logs -f

ps:
	$(COMPOSE) -f $(COMPOSE_FILE) ps

health:
	$(COMPOSE) -f $(COMPOSE_FILE) exec -T postgres_source sh -c "pg_isready -U $$POSTGRES_USER -d $$POSTGRES_DB"
	$(COMPOSE) -f $(COMPOSE_FILE) exec -T postgres_target sh -c "pg_isready -U $$POSTGRES_USER -d $$POSTGRES_DB"

api:
	$(PYTHONPATH_CMD) $(PYTHON) -m uvicorn source_api.main:application --reload

etl:
ifeq ($(strip $(DATE)),)
	$(error Usage: make etl DATE=YYYY-MM-DD)
endif
	$(PYTHONPATH_CMD) $(PYTHON) -m etl.run --date $(DATE)

dagster:
	$(PYTHONPATH_CMD) $(DAGSTER) dev -f $(DAGSTER_FILE)

test:
	$(PYTHONPATH_CMD) $(PYTHON) -m pytest -q
