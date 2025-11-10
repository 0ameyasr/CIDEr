"""Utilities for CIDEr parsing & construction."""

# ==================
# Dependencies
# ==================

import os
import json

from pathlib import Path
from typing import Optional
from src.structs import Block

# ==================
# Utilities
# ==================


def get_cider_script(path: Path | str) -> Optional[str]:
    """Fetch a `.cider` script at `path`."""
    path = Path(path) if isinstance(path, str) else path
    if os.path.isfile(path):
        if path.suffix == ".cider":
            with open(path, "r") as script:
                return script.read()
        else:
            raise ValueError(
                f"Invalid file type at '{path}'. Expected a '.cider' script but got {f'{path.suffix}' or 'no extension'}."
            )
    elif os.path.isdir(path):
        raise IsADirectoryError(
            f"The path '{path}' is a directory, not a '.cider' script."
        )
    else:
        raise FileNotFoundError(
            f"No file found at path '{path}'. Please check that the path is correct."
        )


def tuple_repr(line: str) -> tuple:
    """Split a line into its tuple representation."""
    return tuple([ele.strip() for ele in line.split(":")])


def get_valid_targets(build_path: Path | str = "build.json") -> set:
    with open(build_path, "r") as build:
        data = json.load(build)
        targets = data["targets"]
        return set(targets)
