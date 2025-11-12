"""Translates CIDEr object code notation to target languages."""

import json
import sys

from src.utils import err

def emit(compiled_codex: dict, name: str, target: str, project: str = "builds"):
    """Emit 1st Norm compiled source-target Codex to a file."""
    compiled_codex_obj = json.loads(compiled_codex)
    status = compiled_codex_obj["status"]
    response = compiled_codex_obj["response"]

    if status == "OK":
        with open(f"{project}/{name}.{target}", "w") as buffer:
            buffer.write(response)
    else:
        err("Codex compilation failed:")
        print(response)
        sys.exit(1)
