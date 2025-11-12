"""The parser used for structuring and representing CIDEr in cascaded object notation."""

# ====================
# Dependencies
# ====================

import re
import os
import json
import pandas

from pathlib import Path
from typing import Any

from src.structs import Block
from src.utils import get_cider_script
from src.errors import warn_block_is_hidden, compilation_error

import src.linter as linter
import src.codex as codex
import src.emitter as emitter

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
                blocks.append({"code": line.strip(), "ln": start_ln + 1, "type": 0})
                continue

            # Multiline block
            while ln < n_lines:
                next_line = lines[ln]
                if next_line.strip().startswith("::") and ln != start_ln:
                    break
                block_lines.append(next_line)
                ln += 1

            block_text = "\n".join(block_lines).strip()
            blocks.append({"code": block_text, "ln": start_ln + 1, "type": 1})
            continue
        elif (
            ("::" in line)
            and (not line.startswith("::"))
            and (not line.startswith(">>"))
        ):
            warn_block_is_hidden(ln + 1)

        ln += 1

    return blocks


def chunk(path: Path | str) -> pandas.DataFrame:
    """Chunks CIDEr script at `path` to code blocks."""
    meta = []
    script = get_cider_script(path)
    blocks = _get_code_blocks(script)
    for i, item in enumerate(blocks):
        block = Block(uid=i, code=item["code"], ln=item["ln"], type=item["type"])
        meta.append((block.code, block.raw, block.closed, block.ln, block.type))
    return pandas.DataFrame(meta, columns=["code", "raw", "closed", "ln", "type"])


def parse(path: Path | str):
    """Parse a CIDEr script to object notation."""

    def _flatten(block: str):
        return re.sub(
            r"\s+", " ", " ".join(line.strip() for line in block.splitlines())
        )

    def _n_lines(block: str):
        return len(block.split("\n"))

    code_blocks = chunk(path)
    linter.lint(code_blocks)

    code_objects = []
    for uid in range(len(code_blocks)):
        block = code_blocks.iloc[uid]

        raw = block["raw"]
        ln = block["ln"]

        code_objects.append(
            {
                "uid": int(uid),
                "raw": _flatten(raw),
                "span": (int(ln), int(ln + _n_lines(raw))),
            }
        )

    raw_codex = codex.assemble_codex(code_objects)
    compiled_codex = codex.compile(raw_codex)
    
    target = code_objects[0]["raw"].split(":")[1].strip()
    
    base_name = os.path.basename(path)
    name = os.path.splitext(base_name)[0]
    
    emitter.emit(compiled_codex, name, target)
    return compiled_codex
