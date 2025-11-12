"""Compiler for CIDEr scripts."""

import os
import sys
import argparse
import src.parser as parser
from src.utils import info, err, warn, is_dir_empty, has_files_with_extension
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME")
OLLAMA_MODEL_NAME = os.getenv("OLLAMA_MODEL_NAME")


def main():
    parser_cli = argparse.ArgumentParser(
        description="CIDEr | Cascaded Integrated Development Environment (Scripting Engine)"
    )
    parser_cli.add_argument(
        "path",
        type=str,
        help="Path to a directory containing CIDEr source scripts, or a script file.",
    )
    parser_cli.add_argument(
        "--ollama", action="store_true", help="Use an Ollama model (optional)"
    )
    args = parser_cli.parse_args()
    
    if args.ollama:
        warn(f"You're using an Ollama model, specifically [bold]'{OLLAMA_MODEL_NAME}'[/bold] - expect compilation time to scale with avaiable compute.")
        warn(f"Small Ollama (local) models are also riskier to work with. Please re-check compiled target code before deployment.")

    path = Path(args.path)
    if path.is_dir():
        info(
            f"Path [bold]'{Path(path)}'[/bold] is a directory... searching for a [bold]'.cider'[/bold] subdirectory."
        )
        cider_dir = path / ".cider"
        if cider_dir.exists() and cider_dir.is_dir():
            info(
                f"Found a [bold]'.cider'[/bold] subdirectory under path [bold]'{Path(path)}'[/bold]... checking for nested source files."
            )
            if is_dir_empty(cider_dir):
                err(f"The [bold red]CIDEr[/bold red] source directory [bold](.cider)[/bold] is empty!")
                sys.exit(1)
            else:
                count = has_files_with_extension(cider_dir,".ci")
                if count > 0:
                    info(f"Found {count} [bold red]CIDEr[/bold red] source {'files' if count > 1 else 'file'}... preparing to compile {'them' if count > 1 else 'it'}.")
                    for file in os.listdir(cider_dir):
                        info(f"Compiling [bold]'{Path(file)}'[/bold]...")
                        if file.endswith(".ci"):
                            parser.parse(f"{Path(cider_dir/Path(file))}", ollama=args.ollama, dump=path)
                    info(f"Compiled all source files in [bold]'{Path(cider_dir)}'[/bold]!")
                else:
                    err(f"The [bold]'.cider'[/bold] directory exists but has no [bold red]CIDEr[/bold red] source files.")
                    sys.exit(1)
        else:
            err(
                f"Could not find a [bold]'.cider'[/bold] subdirectory (required) under path [bold]'{Path(path)}'[/bold]!"
            )
            sys.exit(1)
    elif path.is_file():
        info(
            f"Path [bold]'{Path(path)}'[/bold] is a [bold red]CIDEr[/bold red] source file and will be compiled as a standalone script."
        )
        parser.parse(str(path), ollama=args.ollama)
    elif not path.exists():
        err(f"Path [bold]`{Path(path)}`[/bold] does not exist.")
        sys.exit(1)


if __name__ == "__main__":
    main()
