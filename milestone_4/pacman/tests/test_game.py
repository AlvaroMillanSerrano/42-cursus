"""Tests for the game rules (no graphics involved)."""

from __future__ import annotations

import random

from pacman.config import Config, LevelConfig, parse_config
from pacman.entities import ACTIVE, EATEN, WAITING
from pacman.game import (EV_GHOST_EATEN, EV_LEVEL_COMPLETE, EV_PLAYER_DIED,
                         EV_SUPER, EV_TIME_UP, Game)
from pacman.maze import E, N, NONE, opposite


def make_game(**overrides: object) -> Game:
    raw: dict[str, object] = {"levels": [{"width": 21, "height": 15}] * 10}
    raw.update(overrides)
    game = Game(parse_config(raw), random.Random(7))
    game.start_level(0)
    return game


def run(game: Game, seconds: float) -> list[str]:
    kinds: list[str] = []
    for _ in range(int(seconds * 60)):
        kinds += [e.kind for e in game.update(1 / 60)]
    return kinds


def open_dir(game: Game) -> int:
    maze = game.current_maze
    x, y = game.player.cell
    return maze.open_directions(x, y)[0]


def test_level_setup() -> None:
    game = make_game()
    maze = game.current_maze
    assert game.lives == 3 and game.score == 0
    assert game.player.cell == maze.start
    assert game.supers == set(maze.corners)
    assert maze.start not in game.pacgums
    assert len(game.ghosts) == 4
    assert {g.home for g in game.ghosts} == set(maze.corners)
    assert all(g.mode == WAITING for g in game.ghosts)


def test_first_level_is_fixed_and_next_levels_random() -> None:
    a, b = make_game(), make_game()
    b.rng = random.Random(8)  # a real session never shares its RNG
    assert a.current_maze.walls == b.current_maze.walls
    a.start_level(1)
    b.start_level(1)
    assert a.current_maze.walls != b.current_maze.walls


def test_pacgum_count_setting() -> None:
    game = make_game(pacgum=42)
    assert len(game.pacgums) == 42


def test_player_moves_and_eats_pacgums() -> None:
    game = make_game(lives=99)
    game.cheats.enabled = game.cheats.invincible = True
    game.player.press(open_dir(game))
    run(game, 1.0)
    assert game.score > 0 and game.score % 10 == 0


def test_player_stops_at_a_wall() -> None:
    game = make_game()
    maze = game.current_maze
    x, y = game.player.cell
    blocked = [d for d in range(4) if not maze.can_move(x, y, d)][0]
    game.player.press(blocked)
    run(game, 0.5)
    assert game.player.cell == (x, y) and game.player.direction == NONE


def test_instant_reversal_mid_corridor() -> None:
    game = make_game()
    direction = open_dir(game)
    game.player.press(direction)
    game.update(0.03)
    assert game.player.progress > 0
    before = game.player.position
    game.player.press(opposite(direction))
    assert game.player.direction == opposite(direction)
    after = game.player.position
    assert abs(before[0] - after[0]) < 1e-6
    assert abs(before[1] - after[1]) < 1e-6


def test_buffered_turn_is_taken_at_the_next_junction() -> None:
    game = make_game()
    maze = game.current_maze
    player = game.player
    player.press(open_dir(game))
    for _ in range(300):
        game.update(1 / 60)
        if player.progress == 0.0:
            options = [d for d in maze.open_directions(*player.cell)
                       if d not in (player.direction,
                                    opposite(player.direction))]
            if options:
                player.press(options[0])
                game.update(1 / 60)
                assert player.direction == options[0]
                return
    raise AssertionError("no junction found")


def test_held_key_resumes_after_tap() -> None:
    game = make_game()
    p = game.player
    p.press(E)
    p.press(N)
    p.direction = N
    p.release(N)
    assert p.desired == E


def test_super_pacgum_makes_ghosts_edible_and_they_can_be_eaten() -> None:
    game = make_game(points_per_ghost=200)
    corner = game.current_maze.corners[0]
    game.supers.discard(corner)
    game.power_time_left = game.power_duration()
    for g in game.ghosts:
        g.edible = True
        g.mode = ACTIVE
    ghost = game.ghosts[0]
    ghost.place(game.player.cell)
    events = game.update(1 / 60)
    assert any(e.kind == EV_GHOST_EATEN and e.points == 200
               for e in events)
    assert ghost.mode == EATEN and not ghost.edible
    assert game.score >= 200


def test_collecting_a_super_pacgum() -> None:
    game = make_game()
    corner = game.current_maze.corners[0]
    game.ghosts[0].place(game.current_maze.start)  # not waiting on it
    game.player.place(corner)
    events = game.update(1 / 60)
    assert any(e.kind == EV_SUPER for e in events)
    assert game.power_time_left > 0
    assert any(g.edible for g in game.ghosts)
    assert game.score == 50


def test_power_wears_off() -> None:
    game = make_game()
    game.cheats.enabled = game.cheats.invincible = True
    game.power_time_left = 0.5
    for g in game.ghosts:
        g.edible = True
    run(game, 1.0)
    assert game.power_time_left == 0.0
    assert not any(g.edible for g in game.ghosts)


def test_eaten_ghost_returns_home_and_respawns() -> None:
    game = make_game(ghost_respawn_time=1.0)
    ghost = game.ghosts[2]
    ghost.mode = ACTIVE
    ghost.place((game.current_maze.start))
    ghost.mode = EATEN
    ghost.respawn = 1.0
    game.player.place(game.current_maze.corners[3])
    game.player.held = []
    game.cheats.enabled = game.cheats.invincible = True
    run(game, 8.0)
    assert ghost.mode == ACTIVE


def test_touching_a_ghost_costs_a_life() -> None:
    game = make_game()
    ghost = game.ghosts[0]
    ghost.mode = ACTIVE
    ghost.place(game.player.cell)
    events = game.update(1 / 60)
    assert any(e.kind == EV_PLAYER_DIED for e in events)
    assert game.lives == 2


def test_invincibility_cheat() -> None:
    game = make_game()
    game.cheats.enabled = game.cheats.invincible = True
    ghost = game.ghosts[0]
    ghost.mode = ACTIVE
    ghost.place(game.player.cell)
    assert not game.update(1 / 60)
    assert game.lives == 3


def test_cheats_do_nothing_when_disabled() -> None:
    game = make_game()
    game.cheat_extra_life()
    game.cheat_skip_level()
    assert game.lives == 3 and game.pacgums


def test_freeze_cheat_stops_ghosts() -> None:
    game = make_game()
    game.cheats.enabled = game.cheats.freeze = True
    game.cheats.invincible = True
    for g in game.ghosts:
        g.mode = ACTIVE
    before = [g.position for g in game.ghosts]
    run(game, 1.0)
    assert before == [g.position for g in game.ghosts]


def test_skip_level_cheat_completes_the_level() -> None:
    game = make_game(cheat_mode=True)
    game.cheat_skip_level()
    assert EV_LEVEL_COMPLETE in [e.kind for e in game.update(1 / 60)]


def test_eating_everything_completes_the_level() -> None:
    game = make_game()
    game.pacgums = {game.player.cell}
    game.supers = set()
    game.pacgums = {(game.player.x, game.player.y)}
    assert EV_LEVEL_COMPLETE in [e.kind for e in game.update(1 / 60)]


def test_time_up_costs_a_life_and_restart_refills() -> None:
    game = make_game(level_max_time=5)
    kinds = run(game, 5.5)
    assert EV_TIME_UP in kinds or EV_PLAYER_DIED in kinds
    game.lives = 3
    game.restart_level()
    assert game.time_left == 5.0 and len(game.pacgums) > 0


def test_score_never_decreases() -> None:
    game = make_game(lives=99)
    rng = random.Random(1)
    last = 0
    for i in range(60 * 30):
        if i % 20 == 0:
            game.player.press(rng.randrange(4))
        for e in game.update(1 / 60):
            if e.kind in (EV_PLAYER_DIED, EV_TIME_UP):
                game.reset_positions()
        assert game.score >= last
        last = game.score


def test_ghosts_stay_on_free_cells_and_walls() -> None:
    game = make_game(lives=99)
    game.cheats.enabled = game.cheats.invincible = True
    maze = game.current_maze
    for g in game.ghosts:
        g.mode = ACTIVE
    for i in range(60 * 20):
        game.update(1 / 60)
        for g in game.ghosts:
            assert maze.is_free(*g.cell)
            if g.direction != NONE and g.progress > 0:
                assert maze.can_move(g.x, g.y, g.direction)


def test_ghost_speeds_scale_but_stay_below_player() -> None:
    cfg: Config = parse_config({})
    game = Game(cfg, random.Random(1))
    game.level_index = 9
    assert game.ghost_speed() <= cfg.player_speed
    assert game.power_duration() >= 3.0
    assert isinstance(cfg.levels[0], LevelConfig)
