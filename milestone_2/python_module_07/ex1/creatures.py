from ex0.creatures import Creature
from .capabilities import HealCapability, TransformCapability


class Sproutling(Creature, HealCapability):
    def __init__(self, name, c_type):
        super().__init__(name, c_type)

    def attack(self) -> str:
        return f"{self._name()} uses Vine Whip!"

    def heal(self) -> str:
        return f"{self._name()} heals itself for a small amount"


class Bloomelle(Creature, HealCapability):
    def __init__(self, name, c_type):
        super().__init__(name, c_type)

    def attack(self) -> str:
        return f"{self._name()} uses Petal Dance!"

    def heal(self) -> str:
        return f"{self._name()}  heals itself and others for a large amount"


class Shiftling(Creature, TransformCapability):
    def __init__(self, name, c_type):
        super().__init__(name, c_type)

    def attack(self) -> str:
        if self.c_type == "Normal":
            return f"{self._name()} attacks normally."
        else:
            return f"{self._name()} performs a boosted strike!"

    def transform(self) -> str:
        self.c_type = "Sharp"
        return f"{self._name()} shifts into a sharper form!"

    def revert(self) -> str:
        self.c_type = "Normal"
        return f"{self._name()} returns to normal."


class Morphagon(Creature, TransformCapability):
    def __init__(self, name, c_type):
        super().__init__(name, c_type)

    def attack(self) -> str:
        if self.c_type == "Normal/Dragon":
            return f"{self._name()} attacks normally."
        else:
            return f"{self._name()} unleashes a devastating morph strike!"

    def transform(self) -> str:
        self.c_type = "Dragon"
        return f"{self._name()} morphs into a dragonic battle form!"

    def revert(self) -> str:
        self.c_type = "Normal/Dragon"
        return f"{self._name()} stabilizes its form."
