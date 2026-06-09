class Plant:
    def __init__(self, name: str, height: int, age: int):
        self.name = name
        self.height = height
        self.age = age


def get_create_info(plant):
    print(f" Created: {plant.name} ({plant.height}cm, {plant.age} days)")


if __name__ == "__main__":
    plant_data = [
        ("Rose", 25, 30),
        ("Oak", 200, 365),
        ("Cactus", 5, 90),
        ("Sunflower", 80, 45),
        ("Fern", 15, 120),
    ]
    plants = []
    for plant in plant_data:
        plants.append(Plant(plant[0], plant[1], plant[2]))

    print("=== Plant Factory Output ===")
    x = 0
    for plant in plants:
        get_create_info(plant)
        x += 1
    print(f"\nTotal plants created: {x}")
