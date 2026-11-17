# Publishing on itch.io (unlisted/private build)

1. `pip install pyinstaller && make package` -> `dist/pacman-linux.zip`.
2. Create a free project on itch.io, set *Visibility* to **Restricted** or
   **Draft** (unlisted), kind of project **Downloadable**.
3. Upload the zip and tick **Linux**. Or with `butler`:
   `butler push dist/pacman-linux.zip <user>/<game>:linux`
4. Test: download from the private page, unzip, run `./pac-man config.json`.
