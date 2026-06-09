import alchemy
import alchemy.elements


if __name__ == "__main__":
    print("\n=== Sacred Scroll Mastery ===")
    print("\nTesting direct module access:")
    print(
        "alchemy.elements.create_fire(): "
        f"{alchemy.elements.create_fire()}"
    )
    print(
        "alchemy.elements.create_water(): "
        f"{alchemy.elements.create_water()}"
    )
    print(
        "alchemy.elements.create_earth(): "
        f"{alchemy.elements.create_earth()}"
    )
    print(
        "alchemy.elements.create_air(): "
        f"{alchemy.elements.create_air()}"
    )
    print("\nTesting package-level access (controlled by __init__.py):")
    try:
        print(f"alchemy.create_fire(): {alchemy.create_fire()}")
    except Exception:
        print("alchemy.create_fire(): AttributeError - not exposed")
    try:
        print(f"alchemy.create_water(): {alchemy.create_water()}")
    except Exception:
        print("alchemy.create_water(): AttributeError - not exposed")
    try:
        print(f"alchemy.create_earth(): {alchemy.create_earth()}")
    except Exception:
        print("alchemy.create_earth(): AttributeError - not exposed")
    try:
        print(f"alchemy.create_air(): {alchemy.create_air()}")
    except Exception:
        print("alchemy.create_air(): AttributeError - not exposed")
    print("\nPackage metadata:")
    print(f"Version: {alchemy.__version__}")
    print(f"Author:, {alchemy.__author__}")
