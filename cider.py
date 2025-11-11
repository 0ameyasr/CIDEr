"""Compiler for CIDEr scripts."""

import sys
import src.parser as parser
import src.linter as linter

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: cider.py <file>")
    elif len(sys.argv) == 2:
        script = sys.argv[1]
        blocks = parser.chunk(script)
        linter.lint(blocks)

        print("\nCode:")
        for uid in range(len(blocks)):
            print(blocks.iloc[uid]["raw"])
            print()
