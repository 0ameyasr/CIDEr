"""Compiler for CIDEr scripts."""

import sys
import json
import src.parser as parser

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: cider <file>")
    elif len(sys.argv) == 2:
        script = sys.argv[1]
        blocks = parser.parse(script)
        with open("builds/main.json", "w") as main_obj:
            json.dump(blocks, main_obj, indent=4)
