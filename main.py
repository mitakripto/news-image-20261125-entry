"""Entry point for the 25 November 2026 news page.

The program ships one finished image, entry.png, next to this file.
Running it copies those exact bytes to the output location the
harness asks for, so two runs always produce the same file.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def output_path():
    """Where the harness wants entry.png written."""
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if folder:
        return os.path.join(folder, "entry.png")
    return os.path.join("/output", "entry.png")


def main():
    target = output_path()
    folder = os.path.dirname(target)
    if folder:
        os.makedirs(folder, exist_ok=True)
    shutil.copyfile(SOURCE, target)
    print(f"copied {SOURCE} -> {target}")


if __name__ == "__main__":
    main()
