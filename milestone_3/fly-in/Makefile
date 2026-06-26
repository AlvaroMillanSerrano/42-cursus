venv:
	python3 -m venv maze_env
	@echo "activate venv: source maze_env/bin/activate"

install:
	pip install -r requirements.txt

run:
	python3 -m fly-in.main $(MAP)

debug:
	python3 -m pdb fly-in/main.py $(MAP)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

lint:
	-flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	-flake8
	mypy . --strict

.PHONY: install run debug clean lint lint-strict