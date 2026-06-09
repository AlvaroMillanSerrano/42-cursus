import random
import sys
from typing import Any
sys.setrecursionlimit(10000)


class EntryError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class ExitError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class Generator():
    def __init__(self, maze_info: dict[str, Any]):
        self.width: int = maze_info["WIDTH"]
        self.height: int = maze_info["HEIGHT"]
        self.start: tuple[int, int] = maze_info["ENTRY"]
        self.exit: tuple[int, int] = maze_info["EXIT"]
        self.out_file: str = maze_info["OUTPUT_FILE"]
        self.perfect: bool = maze_info["PERFECT"]
        self.cells: list[list[dict[str, Any]]] = []
        self.path: list[tuple[int, int]] = []

    def fill_cells(self) -> None:
        rows = self.height
        cols = self.width

        for _ in range(rows):
            row = []
            for _ in range(cols):
                row.append({
                    "N": 1,
                    "S": 1,
                    "E": 1,
                    "W": 1,
                    "visited": False,
                    "forty_two": False
                })
            self.cells.append(row)

    def create_42(self) -> None:
        width_center = self.width // 2
        height_center = self.height // 2
        forty_two = [
            (height_center - 2, width_center - 3),
            (height_center - 1, width_center - 3),
            (height_center, width_center - 3),
            (height_center, width_center - 2),
            (height_center, width_center - 1),
            (height_center + 1, width_center - 1),
            (height_center + 2, width_center - 1),

            (height_center - 2, width_center + 1),
            (height_center - 2, width_center + 2),
            (height_center - 2, width_center + 3),
            (height_center - 1, width_center + 3),
            (height_center, width_center + 1),
            (height_center, width_center + 2),
            (height_center, width_center + 3),
            (height_center + 1, width_center + 1),
            (height_center + 2, width_center + 1),
            (height_center + 2, width_center + 2),
            (height_center + 2, width_center + 3),
        ]
        for row, cel in forty_two:
            self.cells[row][cel]["visited"] = True
            self.cells[row][cel]["forty_two"] = True

    def cell_exists(self, row_nbr: int, col_nbr: int) -> bool:
        if row_nbr >= self.height or row_nbr < 0:
            return False

        if col_nbr >= self.width or col_nbr < 0:
            return False
        return True

    def check_entry_exit(self) -> None:
        if self.cells[self.start[1]][self.start[0]]["forty_two"]:
            raise EntryError("Entry inside 42 cell")
        if self.cells[self.exit[1]][self.exit[0]]["forty_two"]:
            raise ExitError("Exit inside 42 cell")

    def generate_maze(self, seed: int) -> None:
        s_point = self.start
        self.cells = []
        self.path = []
        self.fill_cells()
        if self.height > 6 and self.width > 8:
            self.create_42()
            self.check_entry_exit()
        if seed == 0:
            seed = random.randint(1, 1000000)
        random.seed(seed)
        self.backtrack_maze(s_point[0], s_point[1])

    def backtrack_maze(self, x: int, y: int) -> None:
        self.cells[y][x]["visited"] = True
        directions = [
            ("N", 0, -1, "S"), ("S", 0, 1, "N"),
            ("E", 1, 0, "W"), ("W", -1, 0, "E")
        ]
        random.shuffle(directions)
        for c_wall, dir_x, dir_y, n_wall in directions:
            neigh_x = x + dir_x
            neigh_y = y + dir_y
            if self.cell_exists(neigh_y, neigh_x):
                neighbour = self.cells[neigh_y][neigh_x]
                if not neighbour["visited"]:
                    self.cells[y][x][c_wall] = 0
                    self.cells[neigh_y][neigh_x][n_wall] = 0
                    self.backtrack_maze(neigh_x, neigh_y)

    def false_matrix(self) -> None:
        for row in self.cells:
            for cell in row:
                if not cell["forty_two"]:
                    cell["visited"] = False

    def path_exit(self) -> None:
        s_point = self.start
        self.false_matrix()
        self.backtrack_path([], s_point[0], s_point[1])

    def backtrack_path(
        self, path: list[tuple[int, int]],
        x: int, y: int
    ) -> bool:
        e_point = self.exit
        c_cell = self.cells[y][x]
        directions = [
            ("N", 0, -1), ("S", 0, 1),
            ("E", 1, 0), ("W", -1, 0)
        ]
        c_cell["visited"] = True
        path.append((x, y))
        if (x, y) == (e_point[0], e_point[1]):
            self.path = list(path)
            path.pop()
            c_cell["visited"] = False
            return True
        for c_wall, dir_x, dir_y in directions:
            if c_cell[c_wall] == 0:
                neigh_x = x + dir_x
                neigh_y = y + dir_y
                n_cell = self.cells[neigh_y][neigh_x]
                if not n_cell["visited"]:
                    if self.backtrack_path(path, neigh_x, neigh_y):
                        path.pop()
                        c_cell["visited"] = False
                        return True
        path.pop()
        c_cell["visited"] = False
        return False

    def render(self, show_path: bool, maze_color: bool) -> None:
        reset = "\033[0m"
        if not maze_color:
            wall_color = "\033[48;5;15m  " + reset
            start_color = "\033[48;5;129m  \033[0m"
            end_color = "\033[48;5;196m  \033[0m"
            path_color = "\033[48;5;75m  \033[0m"
            forty_two_color = "\033[48;5;244m  \033[0m"
        else:
            wall_color = "\033[48;5;34m  " + reset
            start_color = "\033[48;5;82m  \033[0m"
            end_color = "\033[48;5;196m  \033[0m"
            path_color = "\033[48;5;75m  \033[0m"
            forty_two_color = "\033[48;5;244m  \033[0m"
        empty = "  "
        path_set = set(self.path) if show_path else set()
        res = ""
        for y in range(self.height):
            top = ""
            mid = ""
            for x in range(self.width):
                cell = self.cells[y][x]
                top += wall_color
                if cell["N"] == 1:
                    top += wall_color
                elif (x, y) in path_set and (x, y - 1) in path_set:
                    top += path_color
                else:
                    top += empty
                if cell["W"] == 1:
                    mid += wall_color
                elif (x, y) in path_set and (x - 1, y) in path_set:
                    mid += path_color
                else:
                    mid += empty
                if (x, y) == self.start:
                    mid += start_color
                elif (x, y) == self.exit:
                    mid += end_color
                elif cell["forty_two"]:
                    mid += forty_two_color
                elif (x, y) in path_set and show_path:
                    mid += path_color
                else:
                    mid += empty
            res += top + wall_color + "\n"
            res += mid + wall_color + "\n"
        bottom = ""
        for x in range(self.width):
            south_wall = self.cells[self.height - 1][x]["S"]
            bottom += wall_color
            bottom += wall_color if south_wall == 1 else empty
        res += bottom + wall_color + "\n"
        print(res)
