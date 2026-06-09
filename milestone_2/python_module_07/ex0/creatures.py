from abc import ABC, abstractmethod


class Creature(ABC):
    def __init__(self, name: str, c_type: str) -> None:
        self._name: str = name
        self._c_type: str = c_type

    @abstractmethod
    def attack(self) -> str:
        pass

    def describe(self) -> str:
        return f"{self._name} is a {self._c_type} type creature"


class Flameling(Creature):
    def attack(self) -> str:
        return f"{self._name} uses Ember!"


class Pyrodon(Creature):
    def attack(self) -> str:
        return f"{self._name} uses Flamethrower!"


class Aquabub(Creature):
    def attack(self) -> str:
        return f"{self._name} uses Water Gun!"


class Torragon(Creature):
    def attack(self) -> str:
        return f"{self._name} uses Hydro Pump!"
