# Risk analysis

| Risk | Impact | Mitigation | Status |
|------|--------|------------|--------|
| Assigned maze package differs from its README (argument order, coordinate order) | wrong mazes | Keyword arguments, tests on the real behaviour | handled |
| Dead ends remain near the "42" cells even with `perfect=False` | player can be cornered | Instant reversal, ghosts never trapped, documented | handled |
| Generator fails / is replaced at review | crash | `MazeError`, retries, on-screen error screen, tests with a broken generator | handled |
| Config changed during defense with bad values | crash | Clamp + warnings + tests | handled |
| MLX only testable on a machine with X11 | late surprises | Thin backend; game logic fully tested without a window; pygame fallback | open: test on school machine |
| Key input feels laggy | unplayable | Events handled in the same frame, buffered turns, ~1 ms frame cost | handled |
| Highscore file corrupted | crash / data loss | Atomic writes, validation on load | handled |
| Packaging fails on another machine | missing deliverable | `pacman.spec`, `make package`, test on a clean Linux | open |
| Windows dev vs Linux defense | environment mismatch | Develop in WSL/Linux terminal, `make` targets | handled |
