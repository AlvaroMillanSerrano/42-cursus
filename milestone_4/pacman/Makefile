PYTHON    ?= python3
CONFIG    ?= config.json
VENV      ?= .venv
MAZE_WHL  := $(wildcard mazegenerator-*.whl)
MLX_WHL   := $(wildcard mlx-*.whl)
MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports \
             --disallow-untyped-defs --check-untyped-defs

.PHONY: install install-pygame run debug test clean lint lint-strict package

install:
	$(PYTHON) -m pip install -r requirements.txt
	@if [ -n "$(MAZE_WHL)" ]; then $(PYTHON) -m pip install $(MAZE_WHL); \
	else echo "WARNING: no mazegenerator-*.whl found in this directory"; fi
	@if [ -n "$(MLX_WHL)" ]; then $(PYTHON) -m pip install $(MLX_WHL); \
	else echo "NOTE: no mlx-*.whl found; copy it here and re-run 'make install'"; fi

# Optional development backend (Windows/macOS or when MLX is unavailable)
install-pygame:
	$(PYTHON) -m pip install pygame

run:
	$(PYTHON) pac-man.py $(CONFIG)

debug:
	PACMAN_DEBUG=1 $(PYTHON) -m pdb pac-man.py $(CONFIG)

test:
	$(PYTHON) -m pytest -q

clean:
	rm -rf __pycache__ pacman/__pycache__ pacman/backends/__pycache__ \
	       tests/__pycache__ .mypy_cache .pytest_cache build dist \
	       *.egg-info highscores.json

lint:
	flake8 .
	mypy . $(MYPY_FLAGS)

lint-strict:
	flake8 .
	mypy . --strict --ignore-missing-imports

# Builds dist/pacman-linux.zip (needs: pip install pyinstaller)
package:
	$(PYTHON) -m PyInstaller --noconfirm pacman.spec
	rm -rf dist/pacman-linux && mkdir -p dist/pacman-linux
	cp -r dist/pac-man/* dist/pacman-linux/
	cp config.json dist/pacman-linux/config.json
	cp packaging/INGAME_README.txt dist/pacman-linux/README.txt
	cd dist && zip -qr pacman-linux.zip pacman-linux
	@echo "Package ready: dist/pacman-linux.zip"
