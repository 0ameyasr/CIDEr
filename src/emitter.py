"""Translates CIDEr object code notation to target languages."""

import json
import os
from pathlib import Path
from src.utils import err, info, warn


def emit(optimized_code: str, name: str, target: str, project: str = "builds"):
    """Emit 2nd Norm compiled and optimized source-target codex to a file with safe error handling."""
    output_path = os.path.join(project, f"{name}.{target}")
    try:
        with open(output_path, "w", encoding="utf-8") as buffer:
            buffer.write(optimized_code)
        info(f"Optimized Codex emitted successfully: [bold]'{Path(output_path)}'[/bold]")
        return True
    except (OSError, IOError) as e:
        err(f"Failed to write output file [bold]'{Path(output_path)}'[/bold]: {e}")
        return False