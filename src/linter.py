"""Lints CIDEr files before compilation."""

# ====================
# Dependencies
# ====================

import pandas
from src.utils import tuple_repr, get_valid_targets
from src.errors import (
    use_directive_is_absent,
    block_is_invalid,
    script_is_empty,
    use_directive_is_incomplete,
    use_directive_invalid_target,
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


def lint(blocks: pandas.DataFrame) -> bool:
    """Lint all code blocks in a CIDEr script."""
    if blocks.empty:
        script_is_empty()

    n_blocks = len(blocks)
    for uid in range(n_blocks):
        block = blocks.iloc[uid]
        raw = block["raw"]
        valid = block["is_valid"]
        ln = block["ln"]

        if uid == 0:
            try:
                _dir, _lang = tuple_repr(raw)
                _use_present = bool(_dir.lower() == "use")
                if not _use_present:
                    use_directive_is_absent()
                elif _use_present and not _lang:
                    use_directive_is_incomplete()
                elif _use_present and _lang not in TARGETS:
                    use_directive_invalid_target()
            except ValueError:
                use_directive_is_absent()

        if not valid:
            block_is_invalid(uid, ln)
    print("[INFO] All linter checks passed.")
