class PlantNameError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class WaterError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class SunError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


def check_name(name: str) -> None:
    if name is None or name == "":
        raise PlantNameError("Plant name cannot be empty!")


def check_water(water: int) -> None:
    if water < 1:
        raise WaterError(f"Water level {water} is too low (min 1)")
    elif water > 10:
        raise WaterError(f"Water level {water} is too high (max 10)")


def check_sunlight(sunlight: int) -> None:
    if sunlight < 2:
        raise SunError(f" Sunlight hours {sunlight} is too low (min 2)")
    elif sunlight > 12:
        raise SunError(f" Sunlight hours {sunlight} is too high (max 12)")


def check_plant_health(
    plant_name: str,
    water_level: int,
    sunlight_hours: int
) -> None:
    try:
        check_name(plant_name)
        check_water(water_level)
        check_sunlight(sunlight_hours)
    except (PlantNameError, WaterError, SunError) as e:
        print(f"Error: {e}")
    else:
        print(f"Plant '{plant_name}' is healthy!")


def test_plant_checks() -> None:
    print("Testing good values...")
    check_plant_health("tomato", 4, 8)
    print("\nTesting empty plant name...")
    check_plant_health("", 4, 8)
    print("\nTesting bad water level...")
    check_plant_health("melon", 15, 8)
    print("\nTesting bad sunlight hours...")
    check_plant_health("carrot", 8, 0)


if __name__ == "__main__":
    print("=== Garden Plant Health Checker ===\n")
    test_plant_checks()
    print("\nAll error raising tests completed!")
