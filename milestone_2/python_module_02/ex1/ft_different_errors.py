def garden_operations(error_type: str, value: str | int) -> None:
    if error_type == "ValueError":
        print("Testing ValueError...")
        int(value)

    elif error_type == "ZeroDivisionError":
        print("Testing ZeroDivisionError...")
        x = 4 / value

    elif error_type == "FileNotFoundError":
        print("Testing FileNotFoundError...")
        open(value)

    elif error_type == "KeyError":
        print("Testing KeyError...")
        plants = {"a_plant": 5}
        plants[value]

    elif error_type == "MultipleErrors":
        print("Testing multiple errors together...")
        x = int(value)
        z = x / 0
        print(z)


def test_error_types() -> None:
    try:
        garden_operations("ValueError", "abc")
    except ValueError:
        print("Caught ValueError: invalid literal for int()\n")

    try:
        garden_operations("ZeroDivisionError", 0)
    except ZeroDivisionError:
        print("Caught ZeroDivisionError: division by zero\n")

    try:
        value = "missing.txt"
        garden_operations("FileNotFoundError", value)
    except FileNotFoundError:
        print(f"Caught FileNotFoundError: No such file '{value}'\n")

    try:
        value = "_plant"
        garden_operations("KeyError", value)
    except KeyError:
        print(f"Caught KeyError: 'missing\\{value}'\n")

    try:
        garden_operations("MultipleErrors", "abc")
    except (ValueError, ZeroDivisionError):
        print("Caught an error, but program continues!\n")


if __name__ == "__main__":
    print("=== Garden Error Types Demo ===\n")
    test_error_types()
    print("All error types tested successfully!")
