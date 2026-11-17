# PyInstaller spec: builds a self-contained Linux folder of the game.
# Usage: make package   (after: pip install pyinstaller)
from PyInstaller.utils.hooks import collect_all

datas, binaries, hiddenimports = [], [], ["mazegenerator"]
for package in ("mlx", "mazegenerator"):
    try:
        d, b, h = collect_all(package)
        datas += d
        binaries += b
        hiddenimports += h
    except Exception:
        pass  # a package that is not installed is simply skipped

a = Analysis(
    ["pac-man.py"],
    pathex=["."],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports + ["pacman.backends.mlx_backend",
                                   "pacman.backends.pygame_backend"],
    excludes=["tkinter"],
)
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name="pac-man",
          console=True)
coll = COLLECT(exe, a.binaries, a.datas, name="pac-man")
