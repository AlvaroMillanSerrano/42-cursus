import sys
import os
import site


def main() -> None:
    if sys.prefix != sys.base_prefix:
        print(
            "\nMATRIX STATUS: Welcome to the construct",
            f"\nCurrent Python: {sys.executable}",
            f"Virtual Environment: {os.path.basename(sys.prefix)}",
            "\nSUCCESS: You're in an isolated environment!",
            "Safe to install packages without affecting",
            "the global system.",
            "\nPackage installation path:",
            f"{site.getsitepackages()[0]}",
            sep="\n"
        )
    else:
        print(
            "\nMATRIX STATUS: Welcome to the construct",
            f"\nCurrent Python: {sys.executable}",
            "Virtual Environment: None detected",
            "\nWARNING: You're in the global environment!",
            "The machines can see everything you install.",
            "\nTo enter the construct, run:",
            "python -m venv matrix_env",
            "source matrix_env/bin/activate # On Unix",
            "matrix_env\\Scripts\\activate # On Windows",
            "\nThen run this program again.",
            sep="\n"
        )


if __name__ == "__main__":
    main()
