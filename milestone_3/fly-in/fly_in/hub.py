class Hub:
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
        "reset": "\033[0m",
        "crimson": "\033[38;2;220;20;60m",
        "darkred": "\033[38;2;139;0;0m",
        "violet": "\033[38;2;143;0;255m",
    }

    RAINBOW = [
        "\033[91m",
        "\033[38;5;208m",
        "\033[93m",
        "\033[92m",
        "\033[96m",
        "\033[94m",
        "\033[95m"
    ]

    def __init__(self, name: str, x: int, y: int, metadata: str):
        self.name = name
        self.x = x
        self.y = y
        self.metadata = metadata
        metadata_dict = self._parse_metadata(metadata)
        self.zone_type = metadata_dict.get("zone", "normal")
        self.turns_to_enter = 2 if self.zone_type == "restricted" else 1
        self.is_accessible = self.zone_type != "blocked"
        self.is_priority = self.zone_type == "priority"
        if metadata_dict.get("is_start") or metadata_dict.get("is_end"):
            self.max_drones = 9999
        else:
            self.max_drones = int(metadata_dict.get("max_drones", 9999))
        self.color = metadata_dict.get("color") or ""
        self.a_color = Hub.COLOURS.get(self.color, Hub.COLOURS["reset"])
        if self.color == "rainbow":
            self.a_color = ""
        else:
            self.a_color = Hub.COLOURS.get(self.color, Hub.COLOURS["reset"])
        self.a_reset = Hub.COLOURS["reset"]

    def _parse_metadata(self, m_data: str) -> dict[str, str]:
        res: dict[str, str] = {}
        if (
            not m_data
            or not m_data.startswith("[")
            or not m_data.endswith("]")
        ):
            return res
        content = m_data[1:-1]
        pairs = content.replace(",", " ").split()
        for pair in pairs:
            if "=" in pair:
                key, value = pair.split("=", 1)
                res[key.strip()] = value.strip()
        return res

    def draw_rainbow(self, text: str) -> str:
        coloreated_chars = []
        for i, char in enumerate(text):
            color_ansi = Hub.RAINBOW[i % len(Hub.RAINBOW)]
            coloreated_chars.append(f"{color_ansi}{char}")
        return "".join(coloreated_chars) + Hub.COLOURS["reset"]
