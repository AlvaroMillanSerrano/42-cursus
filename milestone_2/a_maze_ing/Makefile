PYTHON = python3
MAIN = a_maze_ing.py
CONFIG = config.txt

venv:
	python3 -m venv maze_env

activate:
	source maze_env/bin/activate

# para instalar dependencias
install:
	pip install -r requirements.txt

# para ejecutar el script principal
run:
	$(PYTHON) $(MAIN) $(CONFIG)

# para ejecutar el script en modo debug con el debugger de Python
debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

# para borrar archivos temporales y cachés
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# para ejecutar flake8 y mypy . con flags concretos
# flake8 .
# revisa estilo de código, formato y algunos errores comunes

# mypy .
# hace chequeo estático de tipos
# Las flags significan, de forma simple:
# --warn-return-any
# 		avisa si una función devuelve Any de forma sospechosa
# --warn-unused-ignores
# 		avisa si pusiste un # type: ignore que realmente no hacía falta
# --ignore-missing-imports
# 		no se queja por ciertos imports que no puede analizar
# --disallow-untyped-defs
# 		no permite funciones sin anotaciones de tipos
# --check-untyped-defs
# 		incluso revisa funciones no tipadas más a fondo

# usamos '-' para que make no se detenga si flake8 falla
lint:
	-flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

# lint-strict como opcional 
lint-strict:
	-flake8
	mypy . --strict

# le dice a make que esas reglas son acciones, no archivos.
.PHONY: install run debug clean lint lint-strict