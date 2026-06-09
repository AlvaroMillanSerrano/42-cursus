class PlantNameError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class WaterError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class WaterTankError(Exception):
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


def check_tank(water_tank: int) -> None:
    if water_tank < 1:
        raise WaterTankError("Not enough water in tank")


class GardenManager():
    def __init__(self):
        self.plants = []
        self.water_tank = 2

    def add_plant(self, name: str, water: int, sunlight: int) -> None:
        try:
            check_name(name)
            check_sunlight(sunlight)
        except (PlantNameError, SunError) as e:
            print(f"Error: {e}")
        else:
            self.plants.append(
                {"name": name, "water": water, "sunlight": sunlight}
            )
            print(f"Added {name} successfully")

    def water_plants(self) -> None:
        print("\nWatering plants...")
        print("Opening watering system")
        try:
            for plant in self.plants:
                check_tank(self.water_tank)
                plant['water'] += 1
                self.water_tank -= 1
                print(f"Watering {plant['name']} - success")
        except WaterTankError as e:
            print(f"Caught GardenError: {e}")
        finally:
            print("Closing watering system (cleanup)")

    def check_plant_health(self) -> None:
        print("\nChecking plant health...")
        for plant in self.plants:
            try:
                check_name(plant['name'])
                check_water(plant['water'])
                check_sunlight(plant['sunlight'])
            except (PlantNameError, WaterError, SunError) as e:
                print(f"Error checking for {plant['name']}: {e}")
            else:
                print(
                    f"{plant['name']}: healthy (water"
                    f"{plant['water']}, sun {plant['sunlight']})"
                )

    def check_recovery(self) -> None:
        try:
            check_tank(self.water_tank)
        except WaterTankError as e:
            print(f"Caught GardenError: {e}")
            print("System recovered and continuing...")


def test_garden_management() -> None:
    manager = GardenManager()
    print("Adding plants to garden...")
    manager.add_plant("tomato", 4, 8)
    manager.add_plant("lettuce", 14, 7)
    manager.add_plant("", 5, 6)
    manager.water_plants()
    manager.check_plant_health()
    print("\nTesting error recovery...")
    manager.check_recovery()


if __name__ == "__main__":
    print("=== Garden Management System ===\n")
    test_garden_management()
    print("\nGarden management system test complete!")
