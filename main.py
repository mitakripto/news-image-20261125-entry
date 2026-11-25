#!/usr/bin/env python3
"""news-image-20261125 entry: emit the 25 November 2026 front page.

draw.py renders the page at build time and the finished image ships beside
this file as entry.png. At grade time this program only copies that file
into the grader's output directory, so repeated runs always agree byte
for byte. Standard library only; nothing is fetched or drawn here.

Try it:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
from pathlib import Path

ENTRY = Path(__file__).resolve().parent / "entry.png"


def run():
    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "entry.png"
    shutil.copyfile(ENTRY, target)
    if target.stat().st_size != ENTRY.stat().st_size:
        raise SystemExit("entry.png did not copy completely")


if __name__ == "__main__":
    run()
