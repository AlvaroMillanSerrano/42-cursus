def validate_ingredients(ingredients: str) -> str:
    valid_ings = {"fire", "water", "earth", "air"}
    l_ing = ingredients.split(" ")
    for ing in l_ing:
        if ing  in valid_ings:
            return f"{ingredients} - VALID"
    return f"{ingredients} - INVALID"
