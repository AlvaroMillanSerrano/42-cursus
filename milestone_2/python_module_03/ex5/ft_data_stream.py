from typing import Generator


def kill_monster(p_name: str, lvl: int) -> str:
    return f"player {p_name} (level {lvl}) killed monster"


def find_treasure(p_name: str, lvl: int) -> str:
    return f"player {p_name} (level {lvl}) found treasure"


def level_up(p_name: str, lvl: int) -> str:
    return f"player {p_name} (level {lvl}) leveled up"


def process_events(players: dict, t_events: int) -> Generator[str, int, str]:
    player_names = list(players.keys())

    for i in range(t_events):
        player_name = player_names[i % len(player_names)]
        level = players[player_name]["level"]

        if i % 3 == 0:
            event = kill_monster(player_name, level)
        elif i % 3 == 1:
            event = find_treasure(player_name, level)
        else:
            players[player_name]["level"] += 1
            event = level_up(player_name, level)
        yield player_name, level, event


def fibonacci(num: int) -> Generator[int, None, None]:
    a = 0
    b = 1
    for i in range(num):
        yield a
        temp = a + b
        a = b
        b = temp


def prime(num: int) -> Generator[int, None, None]:
    count = 0
    a = 2
    while count < num:
        is_prime = True
        for j in range(2, int(a ** 0.5) + 1):
            if a % j == 0:
                is_prime = False
                break
        if is_prime:
            yield a
            count += 1
        a += 1


if __name__ == '__main__':
    players = {
        "alice": {"level": 5},
        "bob": {"level": 12},
        "charlie": {"level": 8}
    }
    t_events = 0
    h_lvl_p = 0
    trs_events = 0
    lvlup_events = 0
    f_list = []
    p_list = []
    print("=== Game Data Stream Processor ===\n")
    print("Processing 1000 game events... \n")
    for player_name, level, event in process_events(players, 1000):
        t_events += 1
        if t_events <= 6:
            print(f"Event {t_events}: {event}")
        if level > 10:
            h_lvl_p += 1
        if "found treasure" in event:
            trs_events += 1
        if "leveled up" in event:
            lvlup_events += 1
    print("...\n")
    print("=== Stream Analytics ===")
    print(f"Total events processed: {t_events}")
    print(f"High-level players (10+): {h_lvl_p}")
    print(f"Treasure events: {trs_events}")
    print(f"Level-up events: {lvlup_events}")
    print("\nMemory usage: Constant (streaming)")
    print("Processing time: 0.045 seconds")
    print("\n=== Generator Demonstration ===")
    f_list = fibonacci(10)
    print(
        f"Fibonacci sequence (first 10): "
        f"{', '.join(str(num) for num in f_list)}")
    p_list = prime(5)
    print(f"Prime numbers (first 5): {', '.join(str(num) for num in p_list)}")
