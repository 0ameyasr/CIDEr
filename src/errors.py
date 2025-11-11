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


def __warn(msg: str):
    print(msg)


def script_is_empty():
    """ERR-000: Raise an error if the script itself is empty or has no recognizable blocks."""
    __err(
        "[L-000/ERR-000] Missing contents: This script has no recognizable CIDEr blocks."
    )


def use_directive_is_absent():
    """ERR-001: Raise an error if the first block (`uid = 0`) does not contain the `use` directive."""
    __err(
        "[L-000/ERR-001] Absent `use`: block #1 must assert the `use` directive for the target language."
    )


def use_directive_is_incomplete():
    """ERR-002: Raise an error if the first block (`uid=0`) contains the `use` directive but is incomplete."""
    __err(
        "[L-000/ERR-002] Incomplete `use`: block #1 asserts the `use` directive, but no target language is specified."
    )


def use_directive_invalid_target(target: str):
    """ERR-003: Raise an error if the first block (`uid=0`) contains the `use` directive but sources an invalid target."""
    __err(
        f"[L-000/ERR-003] Invalid `use` target: block #1 asserts the `use` directive, but aims to source an invalid target `{target}` not in : {TARGETS}."
    )


def block_is_invalid(uid: int, ln: int):
    """L-000/ERR-004: Raise an error if block with `uid` is invalid."""
    __err(
        f"[L-000/ERR-004] Invalid block #{uid+1} (Near line {ln}): this block is empty or has not been closed."
    )


def block_is_not_cascaded(uid: int, ln: int, eln: int):
    """L-001/ERR-000: Raise an error if a multiline block is not cascaded correctly."""
    __err(
        f"[L-001/ERR-000] Out-of-Cascade line {eln} in block #{uid+1} (Near line {ln}): this belongs to a multi-line block that has not been cascaded correctly."
    )


def subject_is_missing(uid: int, ln: int):
    """L-001/ERR-001: Raise an error if a subject in a statement is missing."""
    __err(
        f"[L-001/ERR-001] Subject is unknown for a line in block #{uid+1} (Near line {ln}): this line uses the intent colon but is missing a subject."
    )


def intent_is_missing(uid: int, ln: int):
    """L-001/ERR-002: Raise an error if intent in a statement is missing."""
    __err(
        f"[L-001/ERR-002] Intent is unknown for a line in block #{uid+1} (Near line {ln}): this line uses the intent colon but is missing any intent specifications."
    )


# =====================
# Warnings
# =====================


def warn_block_is_hidden(ln: int):
    """L-000/WARN-000: Warn that any block starting at line `ln` will be ignored."""
    __warn(f"[L-000/WARN-000] The block starting at line {ln} will be ignored.")
