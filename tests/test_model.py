"""Basic validation tests."""

import json

from phir.model import PHIRModel


def test_spec_example():  # noqa: D103
    # From https://github.com/CQCL/phir/blob/main/phir_spec_qasm.md#overall-phir-example-with-quantinuums-extended-openqasm-20
    with open("tests/example.json") as f:
        data = json.load(f)  # type: ignore [misc]

    PHIRModel.model_validate(data)  # type: ignore [misc]
