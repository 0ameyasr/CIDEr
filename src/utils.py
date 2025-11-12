"""Utilities for CIDEr parsing & construction."""

# ==================
# Dependencies
# ==================

import os
import sys
import json

from pathlib import Path
from typing import Optional
from jinja2 import Template
from rich import print

# ==================
# Utilities
# ==================


def get_cider_script(path: Path | str) -> Optional[str]:
    """Fetch a `.ci` script at `path`."""
    path = Path(path) if isinstance(path, str) else path
    if os.path.isfile(path):
        if path.suffix == ".ci":
            with open(path, "r") as script:
                return script.read()
        else:
            raise ValueError(
                f"Invalid file type at '{path}'. Expected a '.ci' script but got {f'`{path.suffix}`' or 'no extension'}."
            )
    elif os.path.isdir(path):
        raise IsADirectoryError(
            f"The path '{path}' is a directory, not a '.ci' script."
        )
    else:
        raise FileNotFoundError(
            f"No file found at path '{path}'. Please check that the path is correct."
        )


def tuple_repr(line: str) -> tuple:
    """Split a line into its tuple representation."""
    return tuple([ele.strip() for ele in line.split(":")])


def get_valid_targets(build_path: Path | str = "build.json") -> set:
    """Get valid targets that can be abstracted by CIDEr based on the configuration."""
    with open(build_path, "r") as build:
        data = json.load(build)
        targets = data["targets"]
        return set(targets)


def bsplit(raw: str):
    """Split a block by the presence of cascaded operators `>>`."""
    return [stmnt.strip() for stmnt in raw.split(">>")]


def get_prompt(task: str, **kwargs):
    """Fetch a prompt from the /prompts/ directory."""
    prompt: str
    with open(f"prompts/{task}.jinja", "r") as prompt_buffer:
        prompt = prompt_buffer.read()
    template: Template = Template(prompt)
    return template.render(**kwargs)

def is_dir_empty(path: str) -> bool:
    """Check if a directory is empty."""
    with os.scandir(path) as entries:
        for _ in entries:
            return False
    return True

def has_files_with_extension(directory: str, extension: str) -> int:
    """Check if files with a certain extension are present in the directory."""
    count = 0
    dir_path = Path(directory)
    for entry in dir_path.iterdir():
        if entry.is_file() and entry.suffix.lower() == extension.lower():
            count += 1
    return count


# ==================
# Print Utilities
# ==================


def err(msg: str):
    """Print an error message."""
    print(f"[bold red][ERR][/bold red] {msg}", file=sys.stderr)


def info(msg: str):
    """Print an informative message."""
    print(f"[bold blue][INFO][/bold blue] {msg}")


def warn(msg: str):
    """Print a warning."""
    print(f"[bold yellow][WARN][/bold yellow] {msg}")
