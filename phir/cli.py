"""PHIR validation driver."""

# mypy: disable-error-code="misc"

import argparse
import importlib.metadata
import json
import sys
from pathlib import Path

from pydantic import ValidationError
from rich import print

from phir.model import PHIRModel


def main() -> None:
    """CLI Entrypoint."""
    parser = argparse.ArgumentParser(
        prog="phir",
        description="Validates and pretty prints valid PHIR",
    )
    parser.add_argument(
        "jsonfile",
        nargs="?",
        help="json file to validate against PHIR spec",
    )
    parser.add_argument(
        "-s",
        "--schema",
        action="store_true",
        default=False,
        help="dump JSON schema of the PHIR model and exit",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f'{importlib.metadata.version("phir")}',
    )
    args = parser.parse_args()

    if args.schema:
        print(json.dumps(PHIRModel.model_json_schema(), indent=2))
        sys.exit(0)

    if args.jsonfile:
        with Path(args.jsonfile).open() as f:
            data = json.load(f)

        try:
            print(PHIRModel.model_validate(data, strict=True))
        except ValidationError as e:
            print(e)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
