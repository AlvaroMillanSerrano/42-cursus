def record_spell(spell_name: str, ingredients: str) -> str:
    from .validator import validate_ingredients
    v_ing = validate_ingredients(ingredients)
    if "INVALID" in v_ing:
        return f"Spell rejected: {spell_name} ({v_ing})"
    return f"Spell recorded: {spell_name} ({v_ing})"
