"""Dataclasses for CIDEr constructs and structures."""

# ====================
# Dependencies
# ====================

import re
from dataclasses import dataclass

# ====================
# Constants
# ====================
CODE_BLOCK = r"::\s*(.*?)\s*::"


@dataclass
class Block:
    """Dataclass representing CIDEr code blocks."""

    uid: int
    code: str
    ln: int
    type: int

    @property
    def closed(self):
        _raw = self.raw.strip()
        _code = self.code.strip()

        if not _raw:
            return False

        if _raw == "::" or _raw == ":::":
            return False

        # return _code.startswith("::") and _code.endswith("::")
        return bool(re.match(CODE_BLOCK, _code, re.DOTALL))

    @property
    def raw(self):
        match = re.search(CODE_BLOCK, self.code, re.DOTALL)
        return match.group(1) if match else self.code
