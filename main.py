"""
Module for copying entry.png to output directory.

This module provides a simple function that copies the generated
`entry.png` image to the directory specified by the
`MAKEFUN_OUTPUT_DIR` environment variable. The behaviour of the
program is unchanged; the docstring is purely informative.
"""
import os
from pathlib import Path

def main():
    src = Path(__file__).with_name("entry.png")
    dest_dir = Path(os.getenv("MAKEFUN_OUTPUT_DIR", "/output"))
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_file = dest_dir / "entry.png"
    dest_file.write_bytes(src.read_bytes())


if __name__ == "__main__":
    main()
