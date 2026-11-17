*This project has been created as part of the 42 curriculum by `amillan- y jaidiaz-`.*

# Pac-Man

## Description

A playable Pac-Man clone written in Python 3.10+. The player crosses
procedurally generated mazes eating pacgums while four ghosts with
different personalities hunt them. The game has 10 levels with a time
limit, super-pacgums that turn the tables on the ghosts, a pause menu, a
persistent top-10 highscore table, a cheat mode for reviewers, and a
packaging recipe for itch.io.

Mazes come from the assigned *A-Maze-ing* package (`mazegenerator`),
used as-is. Graphics use MiniLibX through the 42 `mlx` Python wrapper.

Features: main menu / instructions / highscores / pause menu, HUD (score,
lives, level, time), game-over and victory screens with name entry,
smooth movement with instant key response, four distinct ghost AIs,
robust configuration and highscore handling (no tracebacks).

## Instructions

Requirements: Python >= 3.10, an X11 display (on Windows use WSL2 with
WSLg), and the provided wheels in the repository root.

```bash
make install        # dev tools + mazegenerator-*.whl (+ mlx-*.whl if present)
make run            # python3 pac-man.py config.json
make debug          # same, under pdb
make test           # 67 unit and end-to-end tests
make lint           # flake8 + mypy
make lint-strict    # flake8 + mypy --strict
make package        # PyInstaller build -> dist/pacman-linux.zip
make clean
```

Put the 42 `mlx-*.whl` next to the Makefile before `make install`.
If MLX is unavailable (for development), `make install-pygame` enables an
optional fallback backend; `"backend"` in the config chooses between
`auto` (MLX first), `mlx` and `pygame`. The environment variable
`PACMAN_BACKEND` overrides it.

Controls: arrows or WASD (ZQSD also works) to move, `P`/`ESC` pause,
`ENTER`/`SPACE` to select. Cheat mode: `C` toggles it in game (or set
`"cheat_mode": true`); then `I` invincible, `F` freeze ghosts, `H` fast
player, `N` skip level, `L` extra life.

Rules decided by us: a level is won when **all pacgums and super-pacgums**
are eaten; when the **time runs out** the player loses a life and the
level restarts on the same maze (game over if no lives are left); a ghost
touching the player costs a life and everyone returns to their start
positions.

## Configuration

`python3 pac-man.py config.json` (exactly one argument). The file is JSON
with comments: lines starting with `#`, plus `//` and `/* */`. All keys are
optional; unknown keys are ignored. An invalid type falls back to the
default, an out-of-range number is clamped; each case logs a warning and
the game continues. A missing/unreadable file or broken JSON prints a
clear error and exits with code 1.

| Key | Default | Range | Meaning |
|-----|---------|-------|---------|
| `highscore_filename` | `highscores.json` | non-empty string | Highscore file |
| `lives` | 3 | 1-99 | Starting lives |
| `pacgum` | 0 | 0-5000 | Number of pacgums per level; 0 = every free corridor cell |
| `points_per_pacgum` | 10 | 0-100000 | X |
| `points_per_super_pacgum` | 50 | 0-100000 | Y |
| `points_per_ghost` | 200 | 0-100000 | Z |
| `seed` | 42 | 0-2^31-1 | Seed of level 1 (0 = random). Other levels are random |
| `level_max_time` | 90 | 5-3600 | Seconds per level |
| `power_time` | 8 | 1-60 | Seconds ghosts stay edible (shrinks 0.4 s per level, min 3) |
| `ghost_respawn_time` | 5 | 1-60 | Seconds before an eaten ghost is back |
| `player_speed` | 7.0 | 2-15 | Cells per second |
| `ghost_speed` | 5.5 | 1-15 | Base ghost speed (+0.12 per level, always below the player) |
| `cheat_mode` | false | bool | Start with cheats enabled |
| `backend` | `auto` | auto/mlx/pygame | Graphics backend |
| `levels` | 10 built-in | >= 10 entries | List of `{"width", "height", "seed"?, "time"?}` |

Level size: width 14-61, height 10-41 (14x10 is the smallest maze that
fits the "42" pattern). Fewer than 10 levels are padded with defaults.

## Highscore

`highscores.json` (JSON, path configurable) holds `{"scores": [{"name",
"score"}, ...]}`, sorted, top 10. It is loaded at start and saved when a
name is entered after a win or a loss; the main menu shows the table and
"View Highscores" shows it full screen. Names: ASCII letters, digits and
spaces, max 10 (empty -> `PLAYER`); scores: non-negative integers.
Ties keep the older entry first.

Why: plain JSON is human readable and easy to inspect during review. The
file is written atomically (temp file + `os.replace`) so a crash cannot
truncate it. On load, a missing file gives an empty table, and a corrupt
file or invalid entries are discarded with a warning. A write failure is
reported on the menu and never crashes the game.

## Maze Generation

`pacman/maze.py` is the only module that imports `mazegenerator`. It calls
`MazeGenerator(size=(w, h), perfect=False, entry_cell=(0, 0),
exit_cell=(w-1, h-1), seed=s)` with **keyword arguments** (the package's
README lists a different positional order than its code), and reads
`generator.maze[y][x]`, where bits N=1, E=2, S=4, W=8 mark walls and 15 is
a closed cell (the "42" pattern in the middle).

The adapter: converts the grid into a `Maze` (free cells, passages,
BFS distance maps); keeps only cells connected to the start; starts the
player on the free cell nearest to the centre; puts ghosts and
super-pacgums in the four corners; wraps every failure in `MazeError`
(shown as an on-screen error, never a traceback); retries random mazes up
to 3 times; hides the generator's stdout warnings (logged instead).
Level 1 uses `seed` (reproducible), other levels a random seed.

Known property of the assigned package: even with `perfect=False`, a few
dead ends remain next to the "42" cells. The game copes with them.

## Implementation

* **Movement**: entities walk the maze graph at constant speed
  (cells/second) with sub-cell `progress`. Key presses are handled the same
  frame; a direction pressed early is buffered until the next junction and
  reversing is instant, even mid-corridor.
* **Frame budget**: all drawing goes to a software `Canvas` (a bytearray).
  Walls and pacgums are pre-rendered once per level, so a frame is one
  memcpy plus a handful of sprites (about 1 ms in Python, against a 16 ms
  budget at 60 FPS). The backend then shows one image per frame.
* **Fixed time step**: `Game.update` slices time in steps of at most
  1/60 s, so lag spikes never let entities tunnel through each other.
* **Ghost AI** (BFS distances on the maze): Blinky chases directly; Pinky
  aims 4 cells ahead of the player; Inky mixes chasing with random turns;
  Clyde chases until it is within 8 cells, then retreats to its corner.
  Edible ghosts flee (75 %), eaten ghosts return home as eyes at double
  speed and wait for the respawn timer.
* **Cheats** are plain flags in `Game.cheats`.
* Text uses an embedded 5x7 bitmap font, so no font library is needed.

## General Software Architecture

```
pac-man.py            entry point -> pacman.main.main
pacman/
  main.py             argument check, error handling, wiring
  config.py           JSON-with-comments loader, validation, defaults
  maze.py             adapter to mazegenerator, Maze graph, BFS
  highscores.py       persistent top-10
  entities.py         Mover, Player, Ghost
  ai.py               ghost decisions
  game.py             rules: pellets, scoring, timers, collisions, cheats
  app.py              state machine (menus, ready, play, pause, name entry)
  render.py           scene, HUD and screens drawn on a Canvas
  canvas.py, font.py  software framebuffer and bitmap font
  keys.py             backend independent key names
  backends/           base interface; mlx_backend.py; pygame_backend.py
tests/                pytest suite (config, highscores, maze, game, app)
```

`App` owns a `Game` and a `Renderer`; the `Backend` only opens a window,
forwards key events to `App.key_down/key_up`, calls `App.update/render`
and shows the resulting `Canvas`. `Game` knows nothing about graphics, so
it is fully unit-tested without a window.

## Project Management

See [`docs/project_management/`](docs/project_management/README.md):
timeline, progress, risks, team organisation, acceptance tests and decisions.

## Resources

* Pac-Man ghost behaviour: "The Pac-Man Dossier" (Jamey Pittman).
* Breadth-first search: any graph-algorithms reference (CLRS, ch. 22).
* MiniLibX documentation (42 intranet) and the `mlx` Python wrapper docs.
* Python docs: `json`, `logging`, `dataclasses`, `typing`; PEP 8, PEP 484.
* flake8, mypy, pytest and PyInstaller documentation; itch.io/butler docs.

**Use of AI**: Just check some minor errors
