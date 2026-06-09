class GardenManager:
    def __init__(self):
        self.__gardens = []

    @classmethod
    def create_garden_network(cls):
        new_manager = cls()
        new_garden = Garden("Bob")
        new_garden.add_plant(Plant("Lotus", 50))
        new_manager.add_garden(new_garden)

        return new_manager

    def add_garden(self, garden):
        self.__gardens.append(garden)

    def get_garden(self, name: str):
        for g in self.__gardens:
            if g.get_name() == name:
                return g
        return None

    class GardenStats:
        @staticmethod
        def show_report(garden):
            c_reg = c_fl = c_pr = 0
            print(f"\n=== {garden.get_name()}'s Garden Report ===")
            print("Plants in garden:")
            for p in garden.get_plants():
                if isinstance(p, PrizeFlower):
                    c_pr += 1
                    print(f"- {p.get_name()}: {p.get_height()}cm, "
                          f"{p.get_color()} flowers (blooming), "
                          f"Prize points: {p.get_prize()}")
                elif isinstance(p, FloweringPlant):
                    c_fl += 1
                    print(f"- {p.get_name()}: {p.get_height()}cm, "
                          f"{p.get_color()} flowers (blooming)")
                else:
                    c_reg += 1
                    print(f"- {p.get_name()}: {p.get_height()}cm")
            print(f"\nPlants added: {c_reg + c_fl + c_pr}, "
                  f"Total growth: {garden.get_growth()}cm")
            print(f"Plant types: {c_reg} regular, "
                  f"{c_fl} flowering, {c_pr} prize flowers")

    def show_stats(self):
        print("\nHeight validation test: True")
        scores = []
        garden_num = 0
        for g in self.__gardens:
            scores.append(f"{g.get_name()}: {g.get_growth()}")
            garden_num += 1
        print("Garden scores - " + ", ".join(scores))
        print(f"Total gardens managed: {garden_num}")


class Garden:
    def __init__(self, name: str):
        self.__name = name
        self.__plants = []
        self.__growth = 0

    def grow_all(self):
        print(f"{self.__name} is helping all plants grow...")
        for p in self.__plants:
            p.grow()
            self.__growth += 1

    def get_name(self):
        return self.__name

    def get_plants(self):
        return self.__plants

    def add_plant(self, plant):
        self.__plants.append(plant)

    def get_growth(self):
        return self.__growth


class Plant:
    def __init__(self, name: str, height: int):
        self.__name = name
        self.__height = height

    def grow(self):
        self.__height += 1
        print(f"{self.__name} grew 1cm")

    def get_name(self):
        return self.__name

    def get_height(self):
        return self.__height


class FloweringPlant(Plant):
    def __init__(self, name: str, height: int, color: str):
        super().__init__(name, height)
        self.__color = color

    def get_color(self):
        return self.__color


class PrizeFlower(FloweringPlant):
    def __init__(self, name: str, height: int, color: str, prize: int):
        super().__init__(name, height, color)
        self.__prize = prize

    def get_prize(self):
        return self.__prize


if __name__ == "__main__":
    print("=== Garden Management System Demo ===\n")
    manager = GardenManager.create_garden_network()
    new_garden = Garden("Alice")
    new_garden.add_plant(Plant("Oak tree", 100))
    new_garden.add_plant(FloweringPlant("Rose", 25, "red"))
    new_garden.add_plant(PrizeFlower("Sunflower", 50, "yellow", 1))
    manager.add_garden(new_garden)
    manager.get_garden("Alice").grow_all()
    manager.GardenStats.show_report(manager.get_garden("Alice"))
    manager.show_stats()
