"""PHIR model lives here."""

from __future__ import annotations

from typing import Any, Literal, TypeAlias

from pydantic import BaseModel

# Data Management


class Data(BaseModel):
    """Data Management Base Class."""

    metadata: dict[str, Any] | None = None


class VarDefine(Data):
    """Defining Variables."""

    data_type: str | type
    data: str
    variable: str
    size: int


class CVarDefine(VarDefine):
    """Defining Classical Variables."""

    data: Literal["cvar_define"]

    cvar_id: int | None = None


class QVarDefine(VarDefine):
    """Defining Quantum Variables."""

    data: Literal["qvar_define"]

    qubit_ids: list[int] | None = None


class ExportVar(Data):
    """Exporting Classical Variables."""

    variables: list[str]
    to: list[str] | None = None


DataMgmt: TypeAlias = CVarDefine | QVarDefine | ExportVar

# Operations


class Op(BaseModel):
    """Operation Base Class."""

    args: list[Any] | None = None
    returns: list[Any] | None = None
    metadata: dict[str, Any] | None = None


class QOp(Op):
    """Quantum operation."""

    qop: str
    args: list[list[str | int] | list[list[str | int]]]


class COp(Op):
    """Classical operation."""

    cop: str
    args: list[Any]


class FFCall(COp):
    """External Classical Function Call."""

    cop: Literal["ffcall"]
    function: str


class MOp(Op):
    """Machine operation."""

    mop: str


class EMOp(Op):
    """Error model operation."""

    # NOTE: unused


class SOp(Op):
    """Simulation model."""

    # NOTE: unused


OpType: TypeAlias = FFCall | COp | QOp | MOp


# Blocks


class Block(BaseModel):
    """General block type."""

    block: str
    metadata: dict[str, Any] | None = None


class SeqBlock(Block):
    """A generic sequence block."""

    block: Literal["sequence"]

    ops: list[OpType | BlockType]


class IfBlock(Block):
    """If/else block."""

    block: Literal["if"]

    condition: COp
    true_branch: list[OpType]
    false_branch: list[OpType] | None = None


BlockType: TypeAlias = SeqBlock | IfBlock


class PHIRModel(BaseModel):
    """PHIR model object."""

    format_: str = "PHIR/JSON"
    version: str = "0.1.0"
    metadata: dict[str, Any] | None = None
    ops: list[DataMgmt | OpType | BlockType]
