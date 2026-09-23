from typing import Any


class Connection:
    def __init__(self, hub_1: str, hub_2: str, metadata: dict[str, Any]):
        self.nodes = tuple(sorted((hub_1, hub_2)))
        self.metadata = metadata
        if "max_link_capacity" in metadata:
            self.max_link_capacity = int(metadata["max_link_capacity"])
        else:
            self.max_link_capacity = 9999

    def connects(self, z1: str, z2: str) -> bool:
        return tuple(sorted((z1, z2))) == self.nodes
