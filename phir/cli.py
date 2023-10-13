"""PHIR validation driver."""

import argparse
import json
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
        help="json file to validate against PHIR spec",
    )
    args = parser.parse_args()

    with open(Path(args.jsonfile)) as f:  # type: ignore [misc]
        data = json.load(f)  # type: ignore [misc]

    try:
        print(PHIRModel.model_validate(data, strict=True))  # type: ignore [misc]
    except ValidationError as e:
        print(e)
