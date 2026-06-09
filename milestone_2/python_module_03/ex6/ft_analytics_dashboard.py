if __name__ == '__main__':
    players = {
        "alice": {
            "level": 5,
            "score": 2300,
            "active": True,
            "achievements": {
                "first_kill",
                "level_5_master",
                "treasure_hunter",
                "boss_slayer",
                "speed_runner"
            }
        },
        "bob": {
            "level": 12,
            "score": 1800,
            "active": True,
            "achievements": {
                "first_kill",
                "level_10",
                "explorer"
            }
        },
        "charlie": {
            "level": 8,
            "score": 2150,
            "active": True,
            "achievements": {
                "first_kill",
                "level_8_master",
                "puzzle_solver",
                "boss_slayer",
                "collector",
                "god_killer",
                "sharpshooter"
            }
        },
        "diana": {
            "level": 8,
            "score": 2050,
            "active": False,
            "achievements": {
                "level_8_master",
                "treasure_hunter",
                "boss_slayer",
                "sharpshooter"
            }
        }
    }
    print("=== Game Analytics Dashboard ===")

    print("\n=== List Comprehension Examples ===")
    h_score_p = []
    h_scores = []
    a_players = []
    a_scores = {}
    s_categories = {'high': 3, 'medium': 2, 'low': 1}
    p_achievements = {}
    u_ach = set()
    t_unique_ach = set()
    regions = {'north', 'east', 'central'}
    avg_score = 0
    max_s = 0
    for name, stats in players.items():
        if stats["score"] > 2000:
            h_score_p.append(name)
        h_scores.append(stats["score"] * 2)
        if stats["active"] is True:
            a_players.append(name)
    print(f"High scorers (>2000): {h_score_p}")
    print(f"Scores doubled: {h_scores}")
    print(f"Active players: {a_players}")
    print("\n=== Dict Comprehension Examples ===")
    for name, stats in players.items():
        if stats["active"] is True:
            a_scores[name] = stats["score"]
            p_achievements[name] = len(stats["achievements"])
    print(f"Player scores: {a_scores}")
    print(f"Score categories: {s_categories}")
    print(f"Achievement counts: {p_achievements}")
    print("\n=== Set Comprehension Examples ===")
    s_players = set(players.keys())
    for stats in players.values():
        for ach in stats["achievements"]:
            u_ach.add(ach)
    print(f"Unique players = {s_players}")
    print(f"Unique achievements = {u_ach}")
    print(f"Active regions: {regions}")
    print("\n=== Combined Analysis ===")
    print(f"Total players: {len(players)}")
    for stats in players.values():
        for ach in stats["achievements"]:
            t_unique_ach.add(ach)
    print(f"Total unique achievements: {len(t_unique_ach)}")
    for stats in players.values():
        avg_score += stats["score"]
    avg_score /= len(players)
    print(f"Average score: {avg_score}")
    for name, stats in players.items():
        if stats["score"] > max_s:
            max_n = name
            max_s = stats["score"]
            max_ach = len(stats["achievements"])
    print(f"Top performer: {max_n} ({max_s} points, {max_ach} achievements)")
