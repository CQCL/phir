##############################################################################
#
# Copyright (c) 2023 Quantinuum LLC All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
#
##############################################################################

# mypy: disable-error-code="misc"

"""Basic validation tests."""

import json
from pathlib import Path

from phir.model import PHIRModel


def test_spec_example() -> None:
    """From https://github.com/CQCL/phir/blob/main/spec.md .

    Specifically "Overall PHIR Example with Quantinuum's Extended OpenQASM 2.0"
    """
    with Path("tests/example.json").open() as f:
        data = json.load(f)

    PHIRModel.model_validate(data)


def test_conditional_barrier() -> None:
    """Checks for barriers and qparallel blocks inside conditionals."""
    with Path("tests/cond_barrier_qparallel.json").open() as f:
        data = json.load(f)

    PHIRModel.model_validate(data)
