from .elements import create_fire, create_water, create_air, create_earth


def healing_potion() -> str:
    return (
        "Healing potion brewed with "
        f"{create_fire()} and {create_water()}"
    )


def strength_potion() -> str:
    return (
        "Strength potion brewed with "
        f"{create_earth()} and {create_fire()}"
    )


def invisibility_potion() -> str:
    return (
        "Invisibility potion brewed with "
        f"{create_air()} and {create_water()}"
    )


def wisdom_potion() -> str:
    return (
        "Wisdom potion brewed with all elements: "
        f"{create_fire()} {create_water()}"
        f"{create_air()} {create_earth()}"
    )
