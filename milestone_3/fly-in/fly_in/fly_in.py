from typing import Optional
from fly_in.drone import Drone
from fly_in.connection import Connection
from fly_in.hub import Hub


class FlyIn:
    def __init__(
        self,
        hubs: dict[str, Hub],
        connections: list[Connection],
        drones: list[Drone],
        start_hub_name: str,
        end_hub_name: str
    ):
        self.hubs = hubs
        self.connections = connections
        self.drones = drones
        self.s_hub = start_hub_name
        self.e_hub = end_hub_name
        self.current_turn = 0
        self.graph: dict[str, list[tuple[str, tuple[str, str]]]] = (
            self._build_adjacency_list()
        )
        self.hub_reserv: dict[tuple[str, int], int] = {}
        self.link_reservations: dict[tuple[tuple[str, str], int], int] = {}

    def _build_adjacency_list(
        self
    ) -> dict[str, list[tuple[str, tuple[str, str]]]]:
        """Creates and adjacency list in order to optimize the graph."""
        graph: dict[str, list[tuple[str, tuple[str, str]]]] = {
            name: [] for name in self.hubs
        }
        for conn in self.connections:
            if len(conn.nodes) < 2:
                continue
            u, v = conn.nodes[0], conn.nodes[1]
            u_sorted, v_sorted = sorted((u, v))
            link_key = (u_sorted, v_sorted)
            graph[u].append((v, link_key))
            graph[v].append((u, link_key))
        return graph

    def _get_hub_capacity(self, h_name: str, turn: int) -> int:
        """Returns a hub's capacity during a specific turn."""
        if (h_name, turn) not in self.hub_reserv:
            self.hub_reserv[(h_name, turn)] = self.hubs[h_name].max_drones
        return self.hub_reserv[(h_name, turn)]

    def _get_link_capacity(self, link_key: tuple[str, str], turn: int) -> int:
        """Returns a link's capacity during a specific turn."""
        if (link_key, turn) not in self.link_reservations:
            conn_capacity = len(self.drones)
            for c in self.connections:
                if tuple(sorted(c.nodes)) == link_key:
                    conn_capacity = c.max_link_capacity
                    break
            self.link_reservations[(link_key, turn)] = conn_capacity
        return self.link_reservations[(link_key, turn)]

    def calculate_path_with_time(
        self,
        start_turn: int
    ) -> Optional[list[tuple[str, int]]]:
        """Dijkstra search the path given the space available during the turn.
        Returns a list of tuples: (hub_name, turn_to_land)
        """
        queue = [(0, self.s_hub, start_turn)]
        parent: dict[str, Optional[str]] = {self.s_hub: None}
        arrival_turn_at_node = {self.s_hub: start_turn}
        cost_to_node = {self.s_hub: 0}
        while queue:
            queue.sort(key=lambda x: x[0])
            current_cost, current, current_turn = queue.pop(0)
            if current == self.e_hub:
                path = []
                node: Optional[str] = self.e_hub
                while node is not None:
                    path.append((node, arrival_turn_at_node[node]))
                    node = parent[node]
                return path[::-1]
            for neighbour, link_key in self.graph.get(current, []):
                n_hub = self.hubs[neighbour]
                if not n_hub.is_accessible:
                    continue
                travel_duration = n_hub.turns_to_enter
                next_turn = current_turn + travel_duration
                if self._get_link_capacity(link_key, current_turn) <= 0:
                    continue
                if neighbour not in (self.e_hub, self.s_hub):
                    if self._get_hub_capacity(neighbour, next_turn) <= 0:
                        continue
                movement_weight = 1 if n_hub.is_priority else 25
                new_cost = current_cost + movement_weight

                if (neighbour not in cost_to_node or
                        new_cost < cost_to_node[neighbour]):
                    cost_to_node[neighbour] = new_cost
                    arrival_turn_at_node[neighbour] = next_turn
                    parent[neighbour] = current
                    queue.append((new_cost, neighbour, next_turn))
        return None

    def reserve_path(self, path: list[tuple[str, int]]) -> None:
        """Reserves resources for the exact turn it will be used."""
        for i in range(len(path) - 1):
            curr_hub, curr_turn = path[i]
            next_hub, next_turn = path[i+1]
            u_sorted, v_sorted = sorted((curr_hub, next_hub))
            link_key = (u_sorted, v_sorted)
            curr_cap = self._get_link_capacity(link_key, curr_turn)
            self.link_reservations[(link_key, curr_turn)] = curr_cap - 1
            if next_hub not in (self.e_hub, self.s_hub):
                next_cap = self._get_hub_capacity(next_hub, next_turn)
                self.hub_reserv[(next_hub, next_turn)] = next_cap - 1

    def _format_movement_output(
        self,
        drone: Drone,
        hub_name: str,
        conn_name: Optional[str] = None
    ) -> str:
        """Creates and gives color to the movements."""
        dest_hub = self.hubs[hub_name]
        raw_text = (
            f"{drone.id}-{conn_name}" if conn_name
            else f"{drone.id}-{hub_name}"
        )
        if dest_hub.color == "rainbow":
            return str(dest_hub.draw_rainbow(f"[{raw_text}]"))
        return f"{dest_hub.a_color}[{raw_text}]{dest_hub.a_reset}"

    def run_path(self) -> None:
        """Plans dynamic strategy based on resources and simulates."""
        drone_plans = {}
        current_planning_start_turn = 0
        for d in self.drones:
            path = None
            while not path:
                path = self.calculate_path_with_time(
                    current_planning_start_turn
                )
                if not path:
                    current_planning_start_turn += 1
            self.reserve_path(path)
            drone_plans[d.id] = path
        max_turns = (
            max(path[-1][1] for path in drone_plans.values())
            if drone_plans else 0
        )
        for turn in range(max_turns + 1):
            for d in self.drones:
                d.step_transit()
            turn_movements = []
            for d in self.drones:
                plan = drone_plans[d.id]
                for i in range(len(plan) - 1):
                    curr_hub, curr_turn = plan[i]
                    next_hub, next_turn = plan[i+1]
                    if curr_turn == turn:
                        duration = next_turn - curr_turn
                        conn_name = f"{curr_hub}-{next_hub}"
                        d.transit(next_hub, conn_name, duration)
                        if duration == 1:
                            d.step_transit()
                        display_conn = conn_name if duration > 1 else None
                        mov_out = self._format_movement_output(
                            d, next_hub, display_conn
                        )
                        turn_movements.append(mov_out)
                        break
                    elif curr_turn < turn < next_turn:
                        mov_out = self._format_movement_output(d, next_hub)
                        turn_movements.append(mov_out)
                        break
            if turn_movements:
                self.current_turn += 1
                print(" ".join(turn_movements))
        print(f"Total moves: {self.current_turn}")
