def is_valid_nbr(key: str, value: str) -> bool:
    try:
        value = int(value)
    except ValueError:
        raise ValueError(f"Invalid integer value for '{key}': {value}")
    if value < 0:
            raise ValueError(f"'{key}' must be greater or equal than 0")
    else:
        return True


def validate_bounds(name: str, point: tuple[int, int], width: int, height: int) -> None:
    x, y = point
    if not (0 <= x < width and 0 <= y < height):
        raise ValueError(f"{name} is out of maze bounds")

REQUIRED_KEYS = {
    "WIDTH",
    "HEIGHT",
    "ENTRY",
    "EXIT",
    "OUTPUT_FILE",
    "PERFECT",
    "SEED"
}


def parse_file(file_name: str) -> dict[str, str | int | tuple[int, int] | bool]:
    maze_config: dict[str, str | int | tuple[int, int] | bool] = {}    
    try:
        with open(file_name, "r") as maze_txt:
            for line in maze_txt:
                stripped_line = line.strip()
                if not stripped_line or stripped_line.startswith("#"):
                    continue
                if "=" not in line:
                    raise ValueError(f"Invalid line format: {line}")
                key, value = line.split("=", 1)

                key = key.strip()
                value = value.strip()

                if not key or not value:
                    raise ValueError(f"Invalid line format: {line}")
                
                if key in maze_config:
                    raise ValueError(f"Duplicate key '{key}'")
                
                if (key == "WIDTH" or key == "HEIGHT") and is_valid_nbr(key, value):
                    maze_config[key] = int(value)

                elif key == "ENTRY" or key == "EXIT": # una vez que tenemos el diccionario completo comprobar que entra dentro del rango de width y height
                    try:
                        x, y = value.split(",", 1)
                        x = x.strip()
                        y = y.strip()
                    except ValueError:
                        raise ValueError(f"Invalid format for '{key}': {value}")

                    if is_valid_nbr(key, x) and is_valid_nbr(key, y):
                        maze_config[key] = (int(x), int(y))

                elif key == "OUTPUT_FILE":
                    maze_config[key] = value

                elif key == "PERFECT":
                    if value == "True" or value == "False":
                        maze_config[key] = value == "True"
                    else:
                       raise ValueError("PERFECT must be 'True' or 'False'")
                elif key == "SEED" and is_valid_nbr(key, value):
                    maze_config[key] = int(value)
                else:
                    raise ValueError(f"Unknown config key '{key}'")
                
            missing_keys = REQUIRED_KEYS - maze_config.keys()
            if missing_keys:
                raise ValueError(f"Missing required keys: {missing_keys}")
            
            if maze_config["ENTRY"] == maze_config["EXIT"]:
                raise ValueError("Entry and exit must be different")
            
            validate_bounds("ENTRY", maze_config["ENTRY"], maze_config["WIDTH"], maze_config["HEIGHT"])
            validate_bounds("EXIT", maze_config["EXIT"], maze_config["WIDTH"], maze_config["HEIGHT"])

            if maze_config["WIDTH"] < 3 or maze_config["HEIGHT"] < 3:
                raise ValueError("Maze is too small")

    except Exception as error:
        raise Exception(error) # mejorar los errores.
    else:
        return maze_config
