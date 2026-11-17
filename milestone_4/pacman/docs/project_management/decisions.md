# Technical analysis and decisions

* **Software canvas + one image per frame**: keeps the graphics layer tiny
  (MLX image == one buffer) and fast; text via embedded bitmap font.
* **Graph movement** over the generator's cell/wall model: entities move
  between cell centres, so walls are edges, not tiles.
* **Backends behind an interface**: MLX for the defense; optional pygame
  only for development, limited to features that exist in MLX.
* **Level lost on timeout**: -1 life and restart (subject leaves it open).
* **Level won** when pacgums *and* super-pacgums are all eaten.
* **`pacgum` key** = number of pacgums per level (0 = fill all corridors).
* **Missing/invalid config file or JSON** exits with a message; invalid
  *values* are clamped and the game continues.
