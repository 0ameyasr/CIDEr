"""Dataclasses for CIDEr constructs and structures."""

# ====================
# Dependencies
# ====================

import re
from dataclasses import dataclass


@dataclass
class Block:
    """Dataclass representing CIDEr code blocks."""

    uid: int
    code: str
    ln: int

    @property
    def is_valid(self):
        _raw = self.raw.strip()
        _code = self.code.strip()

        if not _raw:
            return False

        if _raw == "::":
            return False

        return _code.startswith("::") and _code.endswith("::")

    @property
    def raw(self):
        pattern = r"::\s*(.*?)\s*::"
        match = re.search(pattern, self.code)
        return match.group(1) if match else self.code
