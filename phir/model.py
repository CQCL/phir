"""PHIR model lives here."""
from __future__ import annotations

import abc
from typing import Any, Literal, TypeAlias

from pydantic import BaseModel, ConfigDict, Field

# Data Management


class Data(BaseModel, abc.ABC):
    """Data Management Base Class."""

    model_config = ConfigDict(extra="forbid")

    metadata: dict[str, Any] | None = None


class VarDefine(Data, abc.ABC):
    """Defining Variables."""

    data: str
    variable: str
    size: int | None


class CVarDefine(VarDefine):
    """Defining Classical Variables."""

    data: Literal["cvar_define"]
    size: int | None
    data_type: str = "i64"


class QVarDefine(VarDefine):
    """Defining Quantum Variables."""

    data: Literal["qvar_define"]
    size: int = Field(gt=0)
    data_type: str | None = "qubits"


class ExportVar(Data):
    """Exporting Classical Variables."""

    data: Literal["cvar_export"]
    variables: list[str]
    to: list[str] | None = None


DataMgmt: TypeAlias = CVarDefine | QVarDefine | ExportVar

# Operations


class Op(BaseModel, abc.ABC):
    """Operation Base Class."""

    model_config = ConfigDict(extra="forbid")

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


class Block(BaseModel, abc.ABC):
    """General block type."""

    model_config = ConfigDict(extra="forbid")

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
SeqBlock.model_rebuild()  # type: ignore [misc]

# Comments


class Comment(BaseModel):
    """Optional comment."""

    model_config = ConfigDict(extra="forbid")

    c: str = Field(..., alias="//")


class PHIRModel(BaseModel):
    """PHIR model object."""

    # Enabled for extra validation, but can change to 'allow' to preserve data
    # See https://docs.pydantic.dev/latest/concepts/models/#extra-fields
    model_config = ConfigDict(extra="forbid")

    format_: str = Field("PHIR/JSON", alias="format")
    version: str = "0.1.0"
    metadata: dict[str, Any] | None = None
    ops: list[DataMgmt | OpType | BlockType | Comment]
