from .creatures import Flameling, Pyrodon, Aquabub, Torragon
from abc import ABC, abstractmethod
from typing import Any


class CreatureFactory(ABC):
    @staticmethod
    @abstractmethod
    def create_base():
        pass

    @staticmethod
    @abstractmethod
    def create_evolved():
        pass


class FlameFactory(CreatureFactory):
    @staticmethod
    def create_base() -> Any:
        return Flameling("Flameling", "Fire")

    @staticmethod
    def create_evolved() -> Any:
        return Pyrodon("Pyrodon", "Fire")


class AquaFactory(CreatureFactory):
    @staticmethod
    def create_base() -> Any:
        return Aquabub("Aquabub", "Water")

    @staticmethod
    def create_evolved() -> Any:
        return Torragon("Torragon", "Water")
