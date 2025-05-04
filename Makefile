run:
	PYTHONPATH=src python3 src/main.py

lint:
	ruff check .

lint-fix:
	ruff check . --fix

format:
	ruff format .

format-check:
	ruff check .

