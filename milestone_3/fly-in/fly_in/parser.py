from typing import Any


class Parser:
    def get_nb_drones(self, line: str, data: dict[str, Any]) -> dict[str, Any]:
        """checks if the drones info is ok"""
        if "nb_drones" not in line:
            raise ValueError("Starting line doesn't contain drones")
        drones = line.split(":")
        if int(drones[1]) < 1:
            raise ValueError("Invalid number of drones")
        data["nb_drones"] = int(drones[1])
        return data

    def get_start_hub(self, line: str, data: dict[str, Any]) -> dict[str, Any]:
        """checks if the start_hub is ok"""
        if data.get("start_hub") is not None:
            raise ValueError("Only one start hub allowed")
        parts = line.split(":", 1)
        content = parts[1].strip()
        metadata_str = ""
        if "[" in content:
            open_bracket = content.find("[")
            metadata_str = content[open_bracket:].strip()
            content = content[:open_bracket].strip()
        h_content = content.split()
        if len(h_content) < 3:
            raise ValueError("Invalid start hub format")
        h_name = h_content[0]
        try:
            x = int(h_content[1])
            y = int(h_content[2])
        except ValueError:
            raise ValueError("invalid coordinates")
        data["start_hub"] = {
            "name": h_name, "x": x,
            "y": y,
            "metadata": metadata_str
        }
        return data

    def get_end_hub(
        self, line: str,
        data: dict[str, Any]
    ) -> dict[str, Any]:
        """checks if the end_hub is ok"""
        if data.get("end_hub") is not None:
            raise ValueError("Only one end hub allowed")
        parts = line.split(":", 1)
        content = parts[1].strip()
        metadata_str = ""
        if "[" in content:
            open_bracket = content.find("[")
            metadata_str = content[open_bracket:].strip()
            content = content[:open_bracket].strip()
        h_content = content.split()
        if len(h_content) < 3:
            raise ValueError("Invalid end hub format")
        h_name = h_content[0]
        try:
            x = int(h_content[1])
            y = int(h_content[2])
        except ValueError:
            raise ValueError("invalid coordinates")
        data["end_hub"] = {
            "name": h_name,
            "x": x, "y": y,
            "metadata": metadata_str
        }
        return data

    def get_normal_hub(
        self, line: str,
        data: dict[str, Any]
    ) -> dict[str, Any]:
        """checks if the hubs are ok"""
        if "hubs" not in data:
            data["hubs"] = {}
        parts = line.split(":", 1)
        content = parts[1].strip()
        metadata_str = ""
        if "[" in content:
            open_bracket = content.find("[")
            metadata_str = content[open_bracket:].strip()
            content = content[:open_bracket].strip()
        h_content = content.split()
        h_name = h_content[0]
        if h_name in data["hubs"]:
            raise ValueError("duplicated hub name")
        if "-" in h_name:
            raise ValueError(f"hub name cannot contain dashes {h_name}")
        try:
            x = int(h_content[1])
            y = int(h_content[2])
        except ValueError:
            raise ValueError("coordinates must be valid integers")
        data["hubs"][h_name] = {"x": x, "y": y, "metadata": metadata_str}
        return data

    def get_conns(self, line: str, data: dict[str, Any]) -> dict[str, Any]:
        """checks if the connections are ok"""
        if "conns" not in data:
            data["conns"] = []
        if "_seen" not in data:
            data["_seen"] = set()
        parts = line.split(":", 1)
        content = parts[1].strip()
        metadata_dict = {}
        if "[" in content and "]" in content:
            meta_start = content.find("[")
            meta_end = content.find("]")
            meta_string = content[meta_start + 1:meta_end]
            content_nodes = content[:meta_start].strip()
            pairs = meta_string.split(",")
            for pair in pairs:
                if "=" in pair:
                    key, value = pair.split("=", 1)
                    metadata_dict[key.strip()] = value.strip()
            if "max_link_capacity" in metadata_dict:
                try:
                    capacity = int(metadata_dict["max_link_capacity"])
                    if capacity <= 0:
                        raise ValueError("max link capacity must be greater than 0")
                    metadata_dict["max_link_capacity"] = capacity
                except ValueError as e:
                    if "must be greater than 0" in str(e):
                        raise
                    raise ValueError("max link capacity must be a valid number")
        else:
            content_nodes = content
        if "-" not in content_nodes:
            raise ValueError("invalid connection format")
        c_content = content_nodes.split("-", 1)
        node1 = c_content[0].strip()
        node2 = c_content[1].strip()
        if node1 == node2:
            raise ValueError("invalid connection, self loop")
        conn_sorted = tuple(sorted((node1, node2)))
        if conn_sorted in data["_seen"]:
            raise ValueError("duplicated connection")
        data["_seen"].add(conn_sorted)
        data["conns"].append({
            "node1": node1,
            "node2": node2,
            "metadata": metadata_dict
        })
        return data

    COLOURS = {
        "green": "\033[92m",
        "blue": "\033[94m",
        "red": "\033[91m",
        "orange": "\033[38;5;208m",
        "yellow": "\033[93m",
        "cyan": "\033[96m",
        "purple": "\033[38;5;93m",
        "brown": "\033[38;5;94m",
        "gold": "\033[38;5;220m",
        "lime": "\033[38;5;46m",
        "magenta": "\033[95m",
        "reset": "\033[0m"
    }

    def get_color(self, line: str) -> str:
        """gets the color of the hub"""
        if "color=" in line:
            try:
                after_color = line.split("color=")[1]
                color_name = after_color.replace("]", "").split()[0]
                return self.COLOURS.get(color_name, "")
            except IndexError:
                return ""
        return ""

    def parse_data(self, file: str) -> dict[str, Any]:
        """parses all data form file"""
        data: dict[str, Any] = {}
        lines: list[str] = []
        with open(file, "r") as map:
            for line in map:
                cleaned = line.strip()
                if cleaned and not cleaned.startswith("#"):
                    lines.append(cleaned)
        if not lines or not lines[0].startswith("nb_drones"):
            raise ValueError("First line must be 'nb_drones'")
        for line in lines:
            color_prefix = self.get_color(line)
            color_reset = self.COLOURS["reset"] if color_prefix else ""
            if line.startswith("nb_drones"):
                data = self.get_nb_drones(line, data)
                print(f"{color_prefix}{line}{color_reset}\n")
            elif line.startswith("start_hub"):
                data = self.get_start_hub(line, data)
                print(f"{color_prefix}{line}{color_reset}")
            elif line.startswith("end_hub"):
                data = self.get_end_hub(line, data)
                print(f"{color_prefix}{line}{color_reset}")
            elif line.startswith("hub"):
                data = self.get_normal_hub(line, data)
                print(f"{color_prefix}{line}{color_reset}")
            elif line.startswith("connection"):
                data = self.get_conns(line, data)
                print(f"{color_prefix}{line}{color_reset}")
        data.pop("_seen", None)
        return data
