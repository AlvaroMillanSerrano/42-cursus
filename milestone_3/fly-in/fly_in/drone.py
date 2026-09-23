class Drone:
    def __init__(self, id_num: int, start_hub: str):
        self.id = f"D{id_num}"
        self.current_hub = start_hub
        self.transit_connection: str = ""
        self.turns_remaining_in_transit: int = 0
        self.is_delivered: bool = False

    def transit(
        self, to_hub: str,
        connection_name: str,
        duration: int
    ) -> None:
        """action of transiting the drone to a new hub"""
        self.destination_hub = to_hub
        self.transit_connection = connection_name
        self.turns_remaining_in_transit = duration
        self.current_hub = ""

    def step_transit(self) -> bool:
        """transits the drone to a new hub"""
        if self.turns_remaining_in_transit > 0:
            self.turns_remaining_in_transit -= 1
            if self.turns_remaining_in_transit == 0:
                self.current_hub = self.destination_hub
                self.destination_hub = ""
                self.transit_connection = ""
                return True
        return False
