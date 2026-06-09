import ex0
from typing import Any


def fight(creature1: Any, creature2: Any) -> None:
    print("Testing battle")
    print(creature1.describe())
    print(" vs.")
    print(creature2.describe())
    print(creature1.attack())
    print(creature2.attack())


if __name__ == "__main__":
    flameling = ex0.FlameFactory.create_base()
    pyrodon = ex0.FlameFactory.create_evolved()
    aquabub = ex0.AquaFactory.create_base()
    torragon = ex0.AquaFactory.create_evolved()

    print("Testing factory")
    print(flameling.describe())
    print(flameling.attack())
    print(pyrodon.describe())
    print(pyrodon.attack())
    print("\nTesting factory")
    print(aquabub.describe())
    print(aquabub.attack())
    print(torragon.describe())
    print(torragon.attack())
    fight(flameling, aquabub)
