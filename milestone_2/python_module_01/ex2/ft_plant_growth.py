class Plant:
    def __init__(self, name: str, height: int, age: int):
        self.name = name
        self.height = height
        self.age = age


def week_grow(plant: str, growth: int, time: int):
    grow(plant, growth)
    age(plant, time)


def grow(plant, growth: int):
    plant.height += growth


def age(plant, time: int):
    plant.age += time


def get_info(plant):
    print(f"{plant.name}: {plant.height}cm, {plant.age} days old")


if __name__ == "__main__":
    growth = 6
    days = 6
    current_day = 1
    rose = Plant("Rose", 25, 30)
    print(f"=== Day {current_day} ===")
    get_info(rose)
    week_grow(rose, growth, days)
    current_day += days
    print(f"=== Day {current_day} ===")
    get_info(rose)
    print(f"Growth this week: +{growth}cm")
