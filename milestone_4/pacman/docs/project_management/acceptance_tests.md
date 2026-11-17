# Acceptance test plan

Automated: `make test` (67 tests) and `make lint` / `make lint-strict`.

| Area | What is verified | How | Result |
|------|------------------|-----|--------|
| Config | comments `#` `//` `/* */`, defaults, clamping, bad types, missing/invalid file | `tests/test_config.py` | pass |
| Highscores | top 10, ties, name rules, corrupt/missing/unwritable file, atomic save | `tests/test_highscores.py` | pass |
| Maze | reproducible seed, connectivity, border walls, generator crash, retries | `tests/test_maze.py` | pass |
| Rules | movement, instant reversal, buffered turns, pacgums, super-pacgum, ghosts eaten/respawn, lives, time up, cheats, score never decreases | `tests/test_game.py` | pass |
| Flow | menu, game, pause, victory after 10 levels, game over, name entry, error screen | `tests/test_app.py` | pass |

Manual checklist (run on the school Linux machine with MLX):

- [ ] Window opens, menu navigable, `EXIT` closes cleanly
- [ ] Keys respond immediately; window close button works
- [ ] 60 FPS feeling, no flicker
- [ ] Cheat keys C I F H N L behave as documented
- [ ] Highscore survives restarting the game
- [ ] `python3 pac-man.py` (no args) and a missing file print clean messages
- [ ] Packaged build from `make package` starts

Bugs found and fixed: <TODO: list>
