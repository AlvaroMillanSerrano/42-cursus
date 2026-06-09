class Plant:
    def __init__(self, name: str, height: int, age: int):
        self.__name = name
        self.__height = height
        self.__age = age

    def get_name(self):
        return self.__name

    def get_height(self):
        return self.__height

    def get_age(self):
        return self.__age


class Flower(Plant):
    def __init__(self, name: str, height: int, age: int, color: str):
        super().__init__(name, height, age)
        self.__color = color

    def get_color(self):
        return self.__color

    def bloom(self):
        print(f"{self.get_name()} is blooming beautifully!\n")


class Tree(Plant):
    def __init__(self, name: str, height: int, age: int, trunk_diameter: int):
        super().__init__(name, height, age)
        self.__trunk_diameter = trunk_diameter

    def get_diameter(self):
        return self.__trunk_diameter

    def produce_shade(self):
        print(f"{self.get_name()} provides 78 square meters of shade\n")


class Vegetable(Plant):
    def __init__(
        self, name: str,
        height: int,
        age: int,
        harvest_season: str,
        nutritional_value: str
    ):
        super().__init__(name, height, age)
        self.__harvest_season = harvest_season
        self.__nutritional_value = nutritional_value

    def get_season(self):
        return self.__harvest_season

    def get_nutrition(self):
        return self.__nutritional_value

    def nutrition(self):
        print(f"{self.get_name()} is rich in {self.get_nutrition()}\n")


def get_info(p):
    if isinstance(p, Flower):
        print(
            f"{p.get_name()} (Flower): {p.get_height()}cm, "
            f"{p.get_age()} days, {p.get_color()} color"
        )
        p.bloom()
    elif isinstance(p, Tree):
        print(
            f"{p.get_name()} (Tree): {p.get_height()}cm, "
            f"{p.get_age()} days, {p.get_diameter()}cm diameter"
        )
        p.produce_shade()
    elif isinstance(p, Vegetable):
        print(
            f"{p.get_name()} (Vegetable): {p.get_height()}cm, "
            f"{p.get_age()} days, {p.get_season()} harvest"
        )
        p.nutrition()


if __name__ == "__main__":
    plants = []
    plants.append(Flower("Rose", 25, 30, "red"))
    plants.append(Flower("Lotus", 20, 15, "purple"))
    plants.append(Tree("Oak", 500, 1825, 50))
    plants.append(Tree("Spruce", 650, 743, 80))
    plants.append(Vegetable("Tomato", 80, 90, "summer", "vitamin C"))
    plants.append(Vegetable("Lettuce", 60, 45, "spring", "vitamin A"))
    print("=== Garden Plant Types ===")
    for plant in plants:
        get_info(plant)
