"""Compiler for CIDEr scripts."""

import argparse
import src.parser as parser
from src.utils import info
from pathlib import Path


def main():
    parser_cli = argparse.ArgumentParser(
        description="CIDEr | Cascaded Integrated Development Environment (Scripting Engine)"
    )
    parser_cli.add_argument("file", type=str, help="Path to the CIDEr source script.")
    parser_cli.add_argument(
        "--ollama", type=bool, default=False, help="Use an Ollama model (optional)"
    )

    args = parser_cli.parse_args()

    script_path = Path(args.file)

    if not script_path.exists():
        print(f"Error: File '{script_path}' not found.")
        return

    parser.parse(str(script_path), ollama=args.ollama)
    info(f"CIDEr Codex compiled and saved.")


if __name__ == "__main__":
    main()
