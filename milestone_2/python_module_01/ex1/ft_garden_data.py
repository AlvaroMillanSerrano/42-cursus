class Plant:
    def __init__(self, name: str, height: int, age: int):
        self.name = name
        self.height = height
        self.age = age


if __name__ == "__main__":
    plants = []
    plants.append(Plant("Rose", 25, 30))
    plants.append(Plant("Sunflower", 80, 45))
    plants.append(Plant("Cactus", 15, 120))
    print("=== Garden Plant Registry ===")
    for p in plants:
        print(f"{p.name}: {p.height}cm, {p.age} days old")
