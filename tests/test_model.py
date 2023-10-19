##############################################################################
#
# Copyright (c) 2023 Quantinuum LLC All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
#
##############################################################################

"""Basic validation tests."""

import json
from pathlib import Path

from phir.model import PHIRModel


def test_spec_example() -> None:  # noqa: D103
    # From https://github.com/CQCL/phir/blob/main/phir_spec_qasm.md#overall-phir-example-with-quantinuums-extended-openqasm-20
    with Path("tests/example.json").open() as f:
        data = json.load(f)  # type: ignore [misc]

    PHIRModel.model_validate(data)  # type: ignore [misc]
