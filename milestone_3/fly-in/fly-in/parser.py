from typing import Any


def valid_nb_drones(line: str, data: dict[str, Any]) -> dict[str, Any]:
    if not "nb_drones" in line:
        raise ValueError("Starting line doesn't contain drones")
    drones = line.split(":")
    if int(drones[1]) < 1:
        raise ValueError("Invalid number of drones")
    data["nb_drones"] = int(drones[1])
    return data


def valid_start_hub(line: str, data: dict[str, Any]) -> dict[str, Any]:
    if data.get("start_hub") != None:
        raise ValueError("Only one start hub allowed")
    hub = line.split(":")
    hub_data = hub[1].strip().split(" ")
    data["start_hub"] = hub_data
    return data


def valid_end_hub(line: str, data: dict[str, Any]) -> dict[str, Any]:
    if data.get("end_hub") != None:
        raise ValueError("Only one end hub allowed")
    hub = line.split(":")
    hub_data = hub[1].strip().split(" ")
    data["end_hub"] = hub_data
    return data


def valid_normal_hub(line: str, data: dict[str, Any]) -> dict[str, Any]:
    if "hubs" not in data:
        data["hubs"] = {}
    parts = line.split(":", 1)
    h_content = parts[1].strip().split(" ", 1)
    h_name = h_content[0]
    if h_name in data["hubs"].keys():
        raise ValueError ("duplicated hub name")
    h_values = h_content[1].split()
    if len(h_values) != 3:
        print(h_values)
        raise ValueError ("invalid format")
    data["hubs"][h_name] = h_values
    return data


def parse_data(file: str) -> dict[str, Any]:
    data: dict[str, Any] = {}
    lines: list[str] = []
    try:
        with open(file, "r") as map:
            for line in map:
                lines.append(line.strip())
        for line in lines:
            if line == lines[1]:
                data = valid_nb_drones(line, data)
            elif "start_hub" in line:
                data = valid_start_hub(line, data)
            elif "end_hub" in line:
                data = valid_end_hub(line, data)
            elif "hub" in line:
                data = valid_normal_hub(line, data)
        print(data)
    except Exception as e:
        print(f"Error: {e}")
