PAC-MAN
=======

Run:   ./pac-man config.json      (from this folder)

CONTROLS
  Arrow keys or WASD (ZQSD on AZERTY) .... move
  P or ESC ............................... pause / resume
  ENTER or SPACE ......................... select in menus

RULES
  Eat every pacgum to clear the level. Corner super-pacgums make the
  ghosts edible for a few seconds. Touching a ghost costs a life.
  Each level has a time limit; running out of time costs a life and
  replays the level. Clear all 10 levels to win. Your score can be saved
  in the Top 10 when the game ends.

OPTIONS (config.json, JSON with # comments)
  lives, pacgum, points_per_pacgum, points_per_super_pacgum,
  points_per_ghost, level_max_time, power_time, ghost_respawn_time,
  player_speed, ghost_speed, seed, cheat_mode, backend, levels[].
  Missing or invalid values fall back to safe defaults.

CHEAT MODE (for reviewers) - press C in game, or "cheat_mode": true
  I invincible   F freeze ghosts   H fast player
  N skip level   L extra life
