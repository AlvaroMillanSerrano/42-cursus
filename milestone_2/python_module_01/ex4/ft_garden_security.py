class Plant:
    def __init__(self, name: str, height: int, age: int):
        self.__name = name
        self.__height = height
        self.__age = age

    def get_name(self):
        return self.__name

    def get_height(self):
        return self.__height

    def set_height(self, new_height: int):
        if new_height > 0:
            self.__height = new_height
            return 0
        else:
            return 1

    def get_age(self):
        return self.__age

    def set_age(self, new_age: int):
        if new_age > 0:
            self.__age = new_age
            return 0
        else:
            return 1


def update_plant(plant, height: int, age: int):
    if plant.set_height(height) == 1:
        print(f"\nInvalid operation attempted: height {height}cm [REJECTED]")
        print("Security: Negative height rejected")
        return
    if plant.set_age(age) == 1:
        print(f"\nInvalid operation attempted: age {age} days [REJECTED]")
        print("Security: Negative age rejected")
        return
    else:
        print("Plant created: Rose")
        print(f"Height updated: {height}cm [OK]")
        print(f"Age updated: {age}days [OK]")


def get_info(plant):
    print(
        f"\nCurrent plant: {plant.get_name()} "
        f"({plant.get_height()}cm, {plant.get_age()} days)"
    )


if __name__ == "__main__":
    plant = Plant("Rose", 10, 8)
    print("=== Garden Security System ===")
    update_plant(plant, 25, 30)
    update_plant(plant, -5, 10)
    get_info(plant)
