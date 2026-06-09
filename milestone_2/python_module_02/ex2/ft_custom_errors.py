class GardenError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class PlantError(GardenError):
    def __init__(self, message: str):
        super().__init__(message)


class WaterError(GardenError):
    def __init__(self, message: str):
        super().__init__(message)


def raise_plant(status: str) -> None:
    if status == "wilting":
        raise PlantError("The tomato plant is wilting!")


def raise_water(water: int) -> None:
    if water < 1:
        raise WaterError("Not enough water in the tank!")


def check_plant(status: str) -> None:
    try:
        raise_plant(status)
    except PlantError as e:
        print(f"Caught PlantError: {e}\n")


def check_water(water: int) -> None:
    try:
        raise_water(water)
    except WaterError as e:
        print(f"Caught WaterError: {e}\n")


def check_both(water: int, status: str) -> None:
    try:
        raise_plant(status)
    except GardenError as e:
        print(f"Caught a garden error: {e}")
    try:
        raise_water(water)
    except GardenError as e:
        print(f"Caught a garden error: {e}")


if __name__ == "__main__":
    print("=== Custom Garden Errors Demo ===\n")
    print("Testing PlantError...")
    check_plant("wilting")
    print("Testing WaterError...")
    check_water(0)
    print("Testing catching all garden errors...")
    check_both(0, "wilting")
    print("")
    print("All custom error types work correctly!")
