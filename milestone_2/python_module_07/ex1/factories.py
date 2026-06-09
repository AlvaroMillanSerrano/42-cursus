from ex0.factories import CreatureFactory
from .creatures import Sproutling, Bloomelle, Shiftling, Morphagon
from typing import Any


class HealingCreatureFactory(CreatureFactory):
    @staticmethod
    def create_base() -> Any:
        return Sproutling("Sproutling", "Grass")

    @staticmethod
    def create_evolved() -> Any:
        return Bloomelle("Bloomelle", "Grass/Fairy")


class TransformCreatureFactory(CreatureFactory):
    @staticmethod
    def create_base() -> Any:
        return Shiftling("Shiftling", "Normal")

    @staticmethod
    def create_evolved() -> Any:
        return Morphagon("Morphagon", "Normal/Dragon")
