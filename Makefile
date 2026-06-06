.PHONY: install test coverage lint format scan-fixtures

PYTHON ?= python

install:
	$(PYTHON) -m pip install -e .[dev]

test:
	$(PYTHON) -m pytest

coverage:
	$(PYTHON) -m pytest --cov

lint:
	$(PYTHON) -m ruff check .

format:
	$(PYTHON) -m ruff format .

scan-fixtures:
	$(PYTHON) -m anaya.cli.main scan tests/fixtures/python/dirty --no-config --format table
