import sys


class NegativeError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def check_negative(quant: int) -> None:
    if (quant < 0):
        raise NegativeError("Quantity can't be negative")


if __name__ == '__main__':
    inv_len = len(sys.argv)
    inventory = dict()
    total_items = 0
    b_quant = -1
    moderate = dict()
    scarce = dict()
    restock = []
    if inv_len < 2:
        print(
            "No items provided. Usage: python3 "
            "ft_inventory_system.py <item1:qta> <item2:qta> ..."
        )
    else:
        try:
            for i in range(1, inv_len):
                item = sys.argv[i].split(":")
                check_negative(int(item[1]))
                if item[0] in inventory:
                    inventory[item[0]] += int(item[1])
                else:
                    inventory[item[0]] = int(item[1])
        except Exception as e:
            print(f"Error: {e}")
            print(
                "Usage: python3 ft_inventory_system.py "
                "<item1:qta> <item2:qta> ..."
            )
        else:
            print("=== Inventory System Analysis ===")
            for i in inventory.values():
                total_items += i
            print(f"Total items in inventory: {total_items}")
            print(f"Unique item types: {len(inventory.keys())}")
            print("\n=== Current Inventory ===")
            for item, quant in inventory.items():
                if quant == 1:
                    print(
                        f"{item}: {quant} unit "
                        f"({round((quant * 100 / total_items), 1)}%)")
                else:
                    print(
                        f"{item}: {quant} units "
                        f"({round((quant * 100 / total_items), 1)}%)")
            print("\n=== Inventory Statistics ===")
            for item, quant in inventory.items():
                if (b_quant < quant):
                    b_item = item
                    b_quant = quant
            if b_quant == 1:
                print(
                    f"Most abundant: "
                    f"{b_item}, ({b_quant} unit)"
                )
            else:
                print(
                    f"Most abundant: "
                    f"{b_item}, ({b_quant} units)"
                )
            l_quant = None
            for item, quant in inventory.items():
                if l_quant is None or l_quant > quant:
                    l_item = item
                    l_quant = quant
            if quant == 1:
                print(
                    f"Least abundant: "
                    f"{l_item}, ({l_quant} unit)"
                )
            else:
                print(
                    f"Least abundant: "
                    f"{l_item}, ({l_quant} units)"
                )
            print("\n=== Item Categories ===")
            for item, quant in inventory.items():
                if quant > 4:
                    moderate[item] = int(quant)
                else:
                    scarce[item] = int(quant)
            print(f"Moderate: {moderate}")
            print(f"Scarce: {scarce}")
            print("\n=== Management Suggestions ===")
            for item, quant in inventory.items():
                if quant == 1 or quant == 0:
                    restock.append(item)
            print(f"Restock needed: {', '.join(restock)}")
            print("\n=== Dictionary Properties Demo ===")
            print(f"Dictionary keys: {', '.join(inventory.keys())}")
            print(
                f"Dictionary values: "
                f"{', ' .join(str(value) for value in inventory.values())}")
            if "sword" in inventory:
                print("Sample lookup - 'sword' in inventory: True")
            else:
                print("Sample lookup - 'sword' in inventory: False")
