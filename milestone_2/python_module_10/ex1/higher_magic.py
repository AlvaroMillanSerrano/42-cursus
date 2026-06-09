from collections.abc import Callable


def spell_combiner(spell1: Callable, spell2: Callable) -> Callable:
    def mix_spell(target: str, power: int) -> tuple[str, str]:
        return (spell1(target, power), spell2(target, power))
    return mix_spell


def power_amplifier(base_spell: Callable, multiplier: int) -> Callable:
    def p_amplifier(target: str, power: int) -> str:
        a_spell: str = base_spell(target, power * multiplier)
        return a_spell
    return p_amplifier


def conditional_caster(condition: Callable, spell: Callable) -> Callable:
    def c_conditional(target: str, power: int) -> str:
        if condition(target, power):
            g_spell: str = spell(target, power)
            return g_spell
        else:
            return ("Spell fizzled")
    return c_conditional


def spell_sequence(spells: list[Callable]) -> Callable:
    def s_sequence(target: str, power: int) -> list[str]:
        sequence: list[str] = []
        for spell in spells:
            sequence.append(spell(target, power))
        return sequence
    return s_sequence


def fireball(target: str, power: int) -> str:
    return f"Fireball hits {target} for {power} HP"


def heal(target: str, power: int) -> str:
    return f"Heal restores {target} for {power} HP"


def lightning(target: str, power: int) -> str:
    return f"Lightning hits {target} for {power} HP"


def cast_cond(target: str, power: int) -> bool:
    return power > 10


if __name__ == "__main__":
    print("Testing spell combiner...")
    combined = spell_combiner(fireball, heal)
    res = combined("Dragon", 10)
    print(f"Combined spell result: {res[0]}, {res[1]}")
    print("\nTesting power amplifier")
    mega_fireball = power_amplifier(fireball, 2)
    print("Testing power amplifier...")
    print(
        f"-Original: {fireball('Midir', 0)},",
        f"-Amplified: {mega_fireball('Midir', 10)}",
        sep="\n"
    )
    print("\nTesting conditional caster...")
    print("Testing spells 'power > 10'")
    condition = conditional_caster(cast_cond, fireball)
    print(
        f"-Condition fulfilled: {condition('Moonlord', 18)}",
        f"-Not fulfilled: {condition('Moonlord', 5)}",
        sep="\n"
    )
    print("\nTesting spell sequence...")
    spell_seq = spell_sequence([fireball, heal, lightning])
    print(", ".join(spell_seq('Leblanc', 10)))
