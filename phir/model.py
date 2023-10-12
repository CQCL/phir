"""PHIR model lives here."""

import json

from pydantic import BaseModel

# Data Management


class Data(BaseModel):
    """Data Management Base Class."""

    metadata: dict | None = None


class DefineVar(Data):
    """Defining Variables."""

    data_type: str | type
    variable: str
    metadata: dict | None = None


class CVarDefine(DefineVar):
    """Defining Classical Variables."""

    data_type: str | type
    variable: str
    cvar_id: int
    size: int
    metadata: dict | None = None


class QVarDefine(DefineVar):
    """Defining Quantum Variables."""

    data_type: str | type
    variable: str
    size: int
    qubit_ids: list[int]
    metadata: dict | None = None


class ExportVar(Data):
    """Exporting Classical Variables."""

    variables: list[str]
    to: list[str] | None = None
    metadata: dict | None = None


# Operations


class Op(BaseModel):
    """Operation Base Class."""

    name: str
    args: list | None = None
    returns: list | None = None
    metadata: dict | None = None


class QOp(Op):
    """Quantum operation."""

    name: str
    args: list
    returns: list | None = None
    metadata: dict | None = None


class COp(Op):
    """Classical operation."""

    name: str
    args: list
    returns: list | None = None
    metadata: dict | None = None


class FFCall(COp):
    """External Classical Function Call."""


class MOp(Op):
    """Machine operation."""


class EMOp(Op):
    """Error model operation."""


class SOp(Op):
    """Simulation model."""


# Blocks


class Block(BaseModel):
    """General block type."""

    metadata: dict | None = None


class SeqBlock(Block):
    """A generic sequence block."""

    ops: list
    metadata: dict | None = None


class IfBlock(Block):
    """If/else block."""

    condition: COp
    true_branch: list[COp]
    false_branch: list | None = None
    metadata: dict | None = None


class PHIR(BaseModel):
    """PHIR model object."""

    format_: str = "PHIR/JSON"
    version: str = "0.1.0"
    metadata: dict | None = None
    ops: list[Data | Op | Block]


print(  # noqa: T201
    json.dumps(PHIR.model_json_schema(), indent=2),  # type: ignore [misc]
)
