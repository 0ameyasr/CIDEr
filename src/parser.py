"""The parser used for structuring and representing CIDEr in cascaded object notation."""

# ====================
# Dependencies
# ====================

import re

from pathlib import Path
from src.utils import get_cider_script
from typing import Optional, Any

# ====================
# Constants (Patterns)
# ====================

CIDER_BLOCK = r"(?<!:)\s*::\s*(.*?)\s*::(?!:)"

# ====================
# Parser
# ====================


def _get_code_blocks(script: str) -> Optional[list[Any]]:
    """Returns all cascaded code blocks in `script`."""
    return re.findall(CIDER_BLOCK, script, re.DOTALL)


def get_script_code_blocks(path: Path | str) -> Optional[list[str]]:
    """Returns all cascaded code blocks in a script at `path`."""
    script = get_cider_script(path)
    code_blocks = _get_code_blocks(script)
    return code_blocks if code_blocks else None

def parse(path: Path | str):
    """Parses CIDEr script at `path`."""
    code_blocks = get_script_code_blocks(path)
    for block in code_blocks:
        print(block) ; print()
