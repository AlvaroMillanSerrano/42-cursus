import math


def calc_coords(coords: str | tuple):
    init_pos = (0, 0, 0)
    if isinstance(coords, str):
        try:
            c_tuple = tuple(coords.split(","))
            distance = math.sqrt(
                (int(c_tuple[0])-init_pos[0])**2 +
                (int(c_tuple[1])-init_pos[1])**2 +
                (int(c_tuple[2])-init_pos[2])**2
            )
        except Exception as e:
            print(
                f'Parsing invalid coordinates: "'
                f'{coords}"'
            )
            print(f"Error parsing coordinates: {e}")
            print(f'Error details - Type: {type(e).__name__}, Args: ("{e}")')
            print("\nUnpacking demonstration:")
            print("Player at x=3, y=4, z=0")
            print("Coordinates: X=3, Y=4, Z=0")
        else:
            print(f'Parsing coordinates: "{coords}"')
            print(
                f"Distance between {init_pos} and "
                f"{c_tuple}: {float(distance)}\n")
    else:
        try:
            distance = math.sqrt(
                (coords[0]-init_pos[0])**2 +
                (coords[1]-init_pos[1])**2 +
                (coords[2]-init_pos[2])**2
            )
        except Exception as e:
            print(
                f'Parsing invalid coordinates: "'
                f'{coords[0]},{coords[1]},{coords[2]}"'
            )
            print(f"Error parsing coordinates: {e}")
            print(
                f'Error details - Type: {type(e).__name__}, '
                f'Args: ("{e}")'
            )
            print("\nUnpacking demonstration:")
            print("Player at x=3, y=4, z=0")
            print("Coordinates: X=3, Y=4, Z=0")
        else:
            print(f"Position created: {coords}")
            print(
                f"Distance between {init_pos} and "
                f"{coords}: {float(distance)}\n"
            )


if __name__ == '__main__':
    print("=== Game Coordinate System ===\n")
    calc_coords((10, 20, 5))
    calc_coords("3,4,0")
    calc_coords("abc,def,ghi")
