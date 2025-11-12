"""Lints CIDEr files before compilation."""

# ====================
# Dependencies
# ====================

import pandas
from src.utils import tuple_repr, get_valid_targets, bsplit, info
from src.errors import (
    use_directive_is_absent,
    block_is_invalid,
    script_is_empty,
    use_directive_is_incomplete,
    use_directive_invalid_target,
    block_is_not_cascaded,
    subject_is_missing,
    intent_is_missing,
)

# ====================
# Constants (Patterns)
# ====================

CIDER_BLOCK = r"(?<!:)\s*::\s*(.*?)\s*::(?!:)"
TARGETS = get_valid_targets()

# ====================
# Linter
# ====================


def bbreak(block: str):
    """Split a code block into constituent cascaded statements."""
    return block.split(">>")


def bbreak_blocks(blocks: pandas.DataFrame):
    """Split all code blocks in the script into their constituent cascaded statements."""
    return {uid: bbreak(blocks.iloc[uid]) for uid in range(len(blocks))}


def lint(blocks: pandas.DataFrame) -> None:
    """Lint all code blocks in a CIDEr script."""
    if blocks.empty:
        script_is_empty()

    n_blocks = len(blocks)

    # L-000: Check if all blocks are closed and well-formed.
    for uid in range(n_blocks):
        block = blocks.iloc[uid]

        raw = block["raw"]
        valid = block["closed"]
        ln = block["ln"]

        if uid == 0:
            try:
                _lang: str
                _dir: str
                _dir, _lang = tuple_repr(raw)
                _use_present = bool(_dir.lower() == "use")
                if not _use_present:
                    use_directive_is_absent()
                elif _use_present and not _lang:
                    use_directive_is_incomplete()
                elif _use_present and _lang.lower() not in TARGETS:
                    use_directive_invalid_target(_lang)
            except ValueError:
                use_directive_is_absent()

        if not valid:
            block_is_invalid(uid, ln)

    # L-001: Check if all blocks use cascaded statements on multilines.
    for uid in range(n_blocks):
        block = blocks.iloc[uid]
        raw: str = block["raw"]
        btype = block["type"]
        if btype == 1:
            lines = raw.split("\n")
            for i in range(1, len(lines)):
                if not lines[i].startswith(">>"):
                    block_is_not_cascaded(uid, block["ln"], block["ln"] + i)

    # L-002: Check if all statements in the script are in correct format.
    for uid in range(n_blocks):
        block = blocks.iloc[uid]

        btype = block["type"]
        raw = block["raw"]
        sln = block["ln"]
        lines = bsplit(raw)

        for line in lines:
            if ":" in line:
                subject, intent = line.split(":", 1)
                if not subject:
                    subject_is_missing(uid, sln)
                elif not intent:
                    intent_is_missing(uid, sln)

    info("All linter checks passed.")
