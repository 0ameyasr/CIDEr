"""The parser used for structuring and representing CIDEr in cascaded object notation."""

# ====================
# Dependencies
# ====================

import pandas

from pathlib import Path
from typing import Any

from src.structs import Block
from src.utils import get_cider_script

# ====================
# Parser
# ====================


def _get_code_blocks(script: str) -> list[dict[str, Any]]:
    """Parse script into code blocks safely, including malformed/unclosed ones."""
    lines = script.splitlines()
    n_lines = len(lines)
    blocks = []
    ln = 0

    while ln < n_lines:
        line = lines[ln].strip()

        if line.startswith("::"):
            start_ln = ln
            block_lines = [lines[ln]]
            ln += 1

            # Inline block statement
            if line.endswith("::") and len(line) > 2 and not line == "::":
                blocks.append({"code": line.strip(), "ln": start_ln + 1})
                continue

            # Multiline block
            while ln < n_lines:
                next_line = lines[ln]
                if next_line.strip().startswith("::") and ln != start_ln:
                    break
                block_lines.append(next_line)
                ln += 1

            block_text = "\n".join(block_lines).strip()
            blocks.append({"code": block_text, "ln": start_ln + 1})
            continue

        ln += 1

    return blocks


def chunk(path: Path | str):
    """Chunks CIDEr script at `path` to code blocks."""
    meta = []
    script = get_cider_script(path)
    blocks = _get_code_blocks(script)
    for i, item in enumerate(blocks):
        block = Block(uid=i, code=item["code"], ln=item["ln"])
        meta.append((block.raw, block.is_valid, block.ln))
    return pandas.DataFrame(meta, columns=["raw", "is_valid", "ln"])
