class PlantError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


def check_plant(plant: str) -> None:
    if plant is None:
        raise PlantError("Cannot water None - invalid plant!")


def water_plants(plant_list) -> None:
    print("Opening watering system")
    try:
        for plant in plant_list:
            check_plant(plant)
            print(f"Watering {plant}")
    except PlantError as e:
        print(f"Error: {e}")
    finally:
        print("Closing watering system (cleanup)")


def test_watering_system() -> None:
    print("Testing normal watering...")
    water_plants(["tomato", "lettuce", "carrots"])
    print("Watering completed successfully!\n")
    print("Testing with error...")
    water_plants(["tomato", None, "lettuce", "carrots"])
    print("")


if __name__ == "__main__":
    print("=== Garden Watering System ===")
    test_watering_system()
    print("Cleanup always happens, even with errors!")
