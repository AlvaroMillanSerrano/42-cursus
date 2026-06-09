from collections.abc import Callable
from typing import Any


def mage_counter() -> Callable:
    c_count: int = 0

    def count() -> int:
        nonlocal c_count
        c_count += 1
        return c_count
    return count


def spell_accumulator(initial_power: int) -> Callable:
    power: int = initial_power

    def accumulate(added_power: int) -> int:
        nonlocal power
        power += added_power
        return power
    return accumulate


def enchantment_factory(enchantment_type: str) -> Callable:
    def enchant_item(item: str) -> str:
        return f"{enchantment_type} {item}"
    return enchant_item


def memory_vault() -> dict[str, Callable]:
    vault: dict[str, Any] = {}

    def store(key: str, value: int) -> str:
        vault[key] = value
        return f"{value}"

    def recall(key: str) -> str:
        return f"{vault.get(key, 'Memory not found')}"
    return {"store": store, "recall": recall}


if __name__ == "__main__":
    print("Testing mage counter...")
    count_a = mage_counter()
    count_b = mage_counter()
    print(
        f"Counter_a call 1: {count_a()}",
        f"Counter_a call 2: {count_a()}",
        f"Counter_b call 1: {count_b()}",
        sep="\n"
    )
    print("\nTesting spell accumulator...")
    s_accumulator = spell_accumulator(100)
    print("Starting with 100:")
    print(
        f"Base 100, Add 20: {s_accumulator(20)}",
        f"Base 100, Add 30: {s_accumulator(30)}",
        sep="\n"
    )
    print("\nTesting enchantment factory...")
    enchant_fire = enchantment_factory("Flaming")
    enchant_frozen = enchantment_factory("Frozen")
    print(
        f"{enchant_fire('Sword')}",
        f"{enchant_frozen('Shield')}",
        sep="\n"
    )
    print("\nTesting memory vault...")
    vault = memory_vault()
    print(
        f"Store 'secret' = {vault['store']('secret', 42)}",
        f"Recall 'secret': {vault['recall']('secret')}",
        f"Recall 'unknown': {vault['recall']('unknown')}",
        sep="\n"
    )
