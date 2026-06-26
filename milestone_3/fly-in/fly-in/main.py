import sys
from .parser import parse_data


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage make run <map> / python3 main.py <map>")
    else:
        parse_data(sys.argv[1])
