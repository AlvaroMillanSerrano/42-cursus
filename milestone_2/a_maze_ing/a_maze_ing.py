import os
from parser import parse_file
import sys
from backtrack import Generator
from typing import Any, cast


def main() -> None:
    show_path = False
    maze_created = False
    maze_color = False
    opt = 0
    while opt != 5:
        try:
            try:
                if not maze_created:
                    file_name = sys.argv[1]
                    maze_info: dict["str", Any] = parse_file(file_name)
                    generator = Generator(maze_info)
                    generator.generate_maze(maze_info["SEED"])
                    generator.path_exit()
                    maze_created = True
            except Exception as e:
                default_maze = {
                    "WIDTH": 20,
                    "HEIGHT": 15,
                    "ENTRY": (0, 0),
                    "EXIT": (19, 14),
                    "OUTPUT_FILE": "output_maze.txt",
                    "PERFECT": True,
                    "SEED": 42
                }
                generator = Generator(default_maze)
                generator.generate_maze(cast(int, default_maze["SEED"]))
                generator.path_exit()
                maze_created = True
                print(f"Error: {e}")
            finally:
                generator.render(show_path, maze_color)
            print("=== A-Maze-ing ===")
            print("1. Re-generate a new Maze")
            print("2. Show/Hide path from entry to exit")
            print("3. Rotate maze color")
            print("4. Bonus option (we have to discuss what to do)")
            print("5. Quit")
            opt = int(input("Choice? (1-5):"))
            if opt == 1:
                generator.generate_maze(0)
                generator.path_exit()
            elif opt == 2:
                show_path = not show_path
            elif opt == 3:
                maze_color = not maze_color
            if opt > 5 or opt < 1:
                raise ValueError
            if (opt != 5):
                os.system('cls' if os.name == 'nt' else 'clear')
        except Exception:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("invalid option")
            opt = 0
    print("bye")


if __name__ == "__main__":
    main()
