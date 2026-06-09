from collections.abc import Callable
from functools import wraps
import time
from typing import Any


def spell_timer(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Casting {func.__name__}...")
        start_time = time.perf_counter()
        result: Any = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        print(f"Spell completed in {execution_time:.3f} seconds")
        return result
    return wrapper


def power_validator(min_power: int) -> Callable:
    def decorator_factory(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if 'power' in kwargs:
                power = kwargs.get('power')
            else:
                power = args[2]
            if power is not None and int(power) >= min_power:
                return func(*args, **kwargs)
            return "Insufficient power for this spell"
        return wrapper
    return decorator_factory


def retry_spell(max_attempts: int) -> Callable:
    def decorator_factory(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            c_try: int = 0
            while c_try < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception:
                    c_try += 1
                    if c_try < max_attempts:
                        print(
                            "Spell failed, retrying... "
                            f"(attempt {c_try}/{max_attempts})"
                        )
            return (
                f"Spell casting failed after {max_attempts} attempts"
            )
        return wrapper
    return decorator_factory


class MageGuild:
    @staticmethod
    def validate_mage_name(name: str) -> bool:
        if len(name) > 3:
            if all(c.isalpha() or c.isspace() for c in name):
                return True
        return False

    @power_validator(min_power=10)
    def cast_spell(self, spell_name: str, power: int) -> str:
        return f"Successfully cast {spell_name} with {power} power"


@spell_timer
def fireball() -> str:
    time.sleep(3)
    return "Fireball cast!"


@retry_spell(max_attempts=3)
def invalid_spell() -> None:
    raise Exception("Invalid spell...")


@retry_spell(max_attempts=3)
def wagh() -> str:
    return "Waaaaaaagh spelled !"


if __name__ == "__main__":
    print("Testing spell timer...")
    print(f"Result: {fireball()}")
    print("\nTesting retrying spell...")
    print(
        invalid_spell(),
        wagh(),
        sep="\n"
    )
    print("\nTesting MageGuild...")
    guild = MageGuild()
    print(
        MageGuild.validate_mage_name("Rasmodius"),
        MageGuild.validate_mage_name("4"),
        guild.cast_spell('Lighting', 15),
        guild.cast_spell('Lighting', 9),
        sep="\n"
    )
