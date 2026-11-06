FUNCTIONS ?= data/input/functions_definition.json
INPUT ?= data/input/function_calling_tests.json
OUTPUT ?= data/output/function_calls.json

install:
	uv sync --refresh

run:
	uv run python -m src --functions_definition $(FUNCTIONS) --input $(INPUT) --output $(OUTPUT)

debug:
	uv run python -m pdb -m src --functions_definition $(FUNCTIONS) --input $(INPUT) --output $(OUTPUT)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf $(VENV_DIR)

lint:
	-flake8 . --exclude=../.venv,venv,.venv
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	-flake8 . --exclude=../.venv,venv,.venv
	mypy . --strict

.PHONY: install run debug clean lint lint-strict