def ft_seed_inventory(plant, num, p_type):
    if p_type == "packets":
        print(f"{plant.capitalize()} seeds: {num} {p_type} avaiable")
    elif p_type == "grams":
        print(f"{plant.capitalize()} seeds: {num} {p_type} total")
    elif p_type == "area":
        print(f"{plant.capitalize()} seeds: covers {num} square meters")
