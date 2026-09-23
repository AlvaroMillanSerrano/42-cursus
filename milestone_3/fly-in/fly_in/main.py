import sys
from fly_in.parser import Parser
from fly_in.drone import Drone
from fly_in.connection import Connection
from fly_in.hub import Hub
from fly_in.fly_in import FlyIn


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage make run <map> / python3 main.py <map>")
    else:
        try:
            parser = Parser()
            data = parser.parse_data(sys.argv[1])
            drones = []
            hubs = {}
            connections = []
            start_hub = Hub(**data["start_hub"])
            end_hub = Hub(**data["end_hub"])
            hubs[start_hub.name] = start_hub
            hubs[end_hub.name] = end_hub
            for i in range(data["nb_drones"]):
                drones.append(Drone(i, start_hub.name))
            for name, info in data["hubs"].items():
                hubs[name] = Hub(name, **info)
            for conn_dict in data["conns"]:
                items = list(conn_dict.values())
                hub_1 = items[0]
                hub_2 = items[1]
                if len(items) > 2:
                    metadata_conn = items[2]
                else:
                    metadata_conn = {}
                connections.append(Connection(hub_1, hub_2, metadata_conn))
            print()
            fly_in = FlyIn(
                hubs,
                connections,
                drones,
                start_hub.name,
                end_hub.name
            )
            fly_in.run_path()
        except Exception as e:
            print(f" Error: {e}")
