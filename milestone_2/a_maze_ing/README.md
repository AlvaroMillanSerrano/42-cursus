## Setup & Usage

This project uses a virtual environment to keep dependencies isolated.

### 1. Create and activate the environment

```bash
python3 -m venv maze_env
source maze_env/bin/activate
```
Check is it's activated:
```bash
which python
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

verify installation
```bash
pip list
```

### 4. Run the project
```bash
make run
```

### 5. Useful Makefile commands
```bash
make install       # install dependencies
make debug         # run with debugger
make clean         # remove cache files
make lint          #run flake8 + mypy
make lint-strict   #run lints in strict mode
```