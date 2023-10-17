##############################################################################
#
# (c) 2023 @ Quantinuum LLC. All Rights Reserved.
# This software and all information and expression are the property of
# Quantinuum LLC, are Quantinuum LLC Confidential & Proprietary,
# contain trade secrets and may not, in whole or in part, be licensed,
# used, duplicated, disclosed, or reproduced for any purpose without prior
# written permission of Quantinuum LLC.
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

    PHIRModel.model_validate(data, strict=True)  # type: ignore [misc]
