##############################################################################
#
# Copyright (c) 2023 Quantinuum LLC All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
#
##############################################################################

"""PHIR validation driver."""

# mypy: disable-error-code="misc"

import argparse
import json
import sys
from importlib.metadata import version
from pathlib import Path

from pydantic import ValidationError
from rich import print

from phir.model import PHIRModel


def main() -> None:
    """CLI Entrypoint."""
    parser = argparse.ArgumentParser(
        prog="phir-cli",
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
        version=f'{version("phir")}',
    )
    args = parser.parse_args()

    if args.schema:
        print(json.dumps(PHIRModel.model_json_schema(), indent=2))
        sys.exit(0)

    if args.jsonfile:
        with Path(args.jsonfile).open() as f:
            data = json.load(f)

        try:
            print(PHIRModel.model_validate(data))
        except ValidationError as e:
            print(e)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
