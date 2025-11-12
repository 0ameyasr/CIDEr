"""Translates CIDEr object code notation to target languages."""

import json
import os
from pathlib import Path
from src.utils import err, info, warn


def emit(compiled_codex: dict, name: str, target: str, project: str = "builds"):
    """Emit 1st Norm compiled source-target codex to a file with safe error handling."""

    if not compiled_codex:
        err("Empty or null compiled codex provided.")
        return False

    try:
        compiled_codex_obj = (
            compiled_codex if isinstance(compiled_codex, dict) else json.loads(compiled_codex)
        )
    except json.JSONDecodeError as e:
        err(f"Invalid JSON for compiled_codex: {e}")
        return False

    status = compiled_codex_obj.get("status")
    response = compiled_codex_obj.get("response")

    if status is None or response is None:
        err("Compiled codex missing 'status' or 'response' fields.")
        warn(f"Received keys: {list(compiled_codex_obj.keys())}")
        return False

    if status != "OK":
        err("Codex compilation failed:")
        print(response)
        return False

    output_path = os.path.join(project, f"{name}.{target}")
    try:
        with open(output_path, "w", encoding="utf-8") as buffer:
            buffer.write(response)
        info(f"Codex emitted successfully: [bold]'{Path(output_path)}'[/bold]")
        return True
    except (OSError, IOError) as e:
        err(f"Failed to write output file [bold]'{Path(output_path)}'[/bold]: {e}")
        return False
