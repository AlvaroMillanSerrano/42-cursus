import alchemy.grimoire

if __name__ == "__main__":
    print("\n=== Circular Curse Breaking ===")
    print("\nTesting ingredient validation:")
    print(
        'validate_ingredients("fire air"): '
        f'{alchemy.grimoire.validate_ingredients("fire air")}'
    )
    print(
        'validate_ingredients("dragon scales"): '
        f'{alchemy.grimoire.validate_ingredients("dragon scales")}'
    )
    print("\nTesting spell recording with validation:")
    print(
        'record_spell("Fireball", "fire air"): '
        f'{alchemy.grimoire.record_spell("Fireball", "fire air")}'
    )
    print(
        'record_spell("Dark Magic", "shadow"): '
        f'{alchemy.grimoire.record_spell("Dark Magic", "shadow")}'
    )
    print("\nTesting late import technique:")
    from alchemy.grimoire import record_spell
    print(
        'record_spell("Lightning", "air"): '
        f'{record_spell("Lightning", "air")}'
    )
    print("\nCircular dependency curse avoided using late imports!")
    print("All spells processed safely!")
