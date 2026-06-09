def calculate_cell_value(cell: dict) -> int:
    hex_value = 0
    if cell["N"] == 1:
        hex_value += 1
    if cell["E"] == 1:
        hex_value += 2
    if cell["S"] == 1:
        hex_value += 4
    if cell["W"] == 1:
        hex_value += 8
    return hex_value


def maze_to_bits(matrix: list[list[dict]]) -> list[list[int]]:
    maze_bits: list[list[int]] = []
    for row in matrix:
        one_row: list[int] = []
        for cell in row:
            one_row.append(calculate_cell_value(cell))
        maze_bits.append(one_row)
    return maze_bits


def maze_hex(maze_bits: list[list[int]]) -> list[list[str]]:
    hex_maze: list[list[str]] = [
        [format(bit, "X") for bit in row]
        for row in maze_bits
    ]
    return hex_maze


def convert_maze(matrix) -> list[list[str]]:
    return maze_hex(maze_to_bits(matrix))


def create_file(maze_object) -> None:
    #parte 1: crear filas de hexadecimales
    maze_as_hex = convert_maze(maze_object.cells)

    #parte 2: los datos de entrada y salida
    maze_entry = maze_object.start
    maze_exit = maze_object.exit

    #parte 3: direccion de la solucion en: NESW
    #TODO

    with open("output_maze.txt", "w") as file:
        for line in maze_as_hex:
            file.write("".join(line) + "\n")
        file.write("\n")
        file.write(f"{maze_entry[0]},{maze_entry[1]}\n")
        file.write(f"{maze_exit[0]},{maze_exit[1]}\n")





