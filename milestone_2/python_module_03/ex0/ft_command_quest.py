import sys

if __name__ == '__main__':
    i = len(sys.argv)
    print("=== Command Quest ===")
    if i == 1:
        print("No arguments provided!")
    print(f"Program name: {sys.argv[0]}")
    if i > 1:
        print(f"Arguments received: {i - 1}")
        for n in range(1, i):
            print(f"Argument {n}: {sys.argv[n]}")
    print(f"Total arguments: {i}\n")
