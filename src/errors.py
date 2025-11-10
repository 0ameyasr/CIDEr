"""Errors raised by CIDEr validation."""

# ====================
# Dependencies
# ====================

import sys
from src.utils import get_valid_targets

# ====================
# Constants
# ====================

TARGETS = get_valid_targets()

# ====================
# Errors
# ====================


def __err(msg: str):
    """Sends the error message to `stderr`."""
    print(msg, file=sys.stderr)
    sys.exit(1)


def script_is_empty():
    """ERR-000: Raise an error if the script itself is empty or has no recognizable blocks."""
    __err(f"[ERR-000] Missing contents: This script has no recognizable CIDEr blocks.")


def use_directive_is_absent():
    """ERR-001: Raise an error if the first block (`uid = 0`) does not contain the `use` directive."""
    __err(
        f"[ERR-001] Absent `use`: block #0 must assert the `use` directive for the target language."
    )


def use_directive_is_incomplete():
    """ERR-002: Raise an error if the first block (`uid=0`) contains the `use` directive but is incomplete."""
    __err(
        f"[ERR-002] Incomplete `use`: block #0 asserts the `use` directive, but no target language is specified."
    )


def use_directive_invalid_target():
    """ERR-003: Raise an error if the first block (`uid=0`) contains the `use` directive but sources an invalid target."""
    __err(
        f"[ERR-003] Invalid `use` target: block #0 asserts the `use` directive, but aims to source an invalid target not in : {TARGETS}."
    )


def block_is_invalid(uid: int, ln: int):
    """ERR-003: Raise an error if block with `uid` is invalid."""
    __err(
        f"[ERR-003] Invalid block #{uid} (Near line {ln}): this block is empty or has not been closed."
    )
