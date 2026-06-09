def check_temperature(temp_str: str) -> int | None:
    print(f"Testing temperature: {temp_str}")
    if temp_str is None:
        print(f"Error: '{temp_str}' is not a valid number\n")
        return
    try:
        temp: int = int(temp_str)
    except ValueError:
        print(f"Error: '{temp_str}' is not a valid number\n")
        return
    if temp < 0:
        print(f"Error: {temp}°C is too cold for plants (min 0°C)\n")
        return
    elif temp > 40:
        print(f"Error: {temp}°C is too hot for plants (max 40°C)\n")
        return
    print(f"Temperature {temp}°C is perfect for plants!\n")
    return temp


if __name__ == "__main__":
    print("=== Garden Temperature Checker ===\n")
    check_temperature("25")
    check_temperature("abc")
    check_temperature("100")
    check_temperature("-50")
    print("All tests completed - program didn't crash!")
