def ft_harvest_total():
    x = int(1)
    harvest = int(0)
    while x <= 3:
        harvest += int(input(f"Day {x} harvest: "))
        x += 1
    print(f"Total harvest: {harvest}")
