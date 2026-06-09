from functools import reduce, partial, lru_cache, singledispatch
from operator import add, mul
from collections.abc import Callable
from typing import Any


def spell_reducer(spells: list[int], operation: str) -> int:
    if not spells:
        return 0
    ops: dict[str, Callable[[int, int], int]] = {
        "add": add,
        "multiply": mul,
        "max": max,
        "min": min
    }
    if operation not in ops:
        raise ValueError(f"Error: invalid operation {operation}")
    return reduce(ops[operation], spells)


def partial_enchanter(base_enchantment: Callable) -> dict[str, Callable]:
    enchant_fire = partial(base_enchantment, 50, "fire")
    enchant_ice = partial(base_enchantment, 50, "ice")
    enchant_lightning = partial(base_enchantment, 50, "lightning")
    return {
        "enchant_fire": enchant_fire,
        "enchant_ice": enchant_ice,
        "enchant_lightining": enchant_lightning
    }


def enchant(power: int, element: str, target: str) -> str:
    return f"{element} enchanted to {target} with {power} power"


@lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    if n < 0:
        return 0
    if n < 2:
        return n
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> Callable[[Any], str]:
    @singledispatch
    def cast_spell(spell: Any) -> str:
        return "Unknown spell type"

    @cast_spell.register(int)
    def _(spell: int) -> str:
        return f"Damage spell: {spell} damage"

    @cast_spell.register(str)
    def _(spell: str) -> str:
        return f"Enchantment: {spell}"

    @cast_spell.register(list)
    def _(spell: list[Any]) -> str:
        return f"Multi-cast: {len(spell)} spells"

    return cast_spell


if __name__ == "__main__":
    print("\nTesting spell reducer...")
    spells = [40, 30, 20, 10]
    try:
        print(
            f"Sum: {spell_reducer(spells, 'add')}",
            f"Product: {spell_reducer(spells, 'multiply')}",
            f"Max: {spell_reducer(spells, 'max')}",
            sep="\n"
        )
    except Exception as e:
        print(e)
    print("\nTesting partial enchanter...")
    enchanters = partial_enchanter(enchant)
    for enchanter in enchanters.values():
        print(enchanter("sword"))
    print("\nTesting memoized fibonacci...")
    print(
        f"Fib(0): {memoized_fibonacci(0)}",
        f"Fib(1): {memoized_fibonacci(1)}",
        f"Fib(10): {memoized_fibonacci(10)}",
        f"Fib(15): {memoized_fibonacci(15)}",
        sep="\n"
    )
    print("\nTesting spell dispatcher...")
    dispatch = spell_dispatcher()
    print(
        dispatch(42),
        dispatch("fireball"),
        dispatch([1, 2, 3]),
        dispatch(3.14),
        sep="\n"
    )
