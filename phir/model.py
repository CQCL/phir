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

"""PHIR model lives here."""
from __future__ import annotations

import abc
from typing import Annotated, Any, Literal, TypeAlias

from pydantic import BaseModel, ConfigDict, Field

Idx: TypeAlias = Annotated[int, Field(ge=0)]
Sym: TypeAlias = str
Bit: TypeAlias = Annotated[list[Sym | Idx], Field(max_length=2)]

# Data Management


class Data(BaseModel, abc.ABC):
    """Data Management Base Class."""

    model_config = ConfigDict(extra="forbid")

    metadata: dict[str, Any] | None = None


class CVarDefine(Data):
    """Defining Classical Variables."""

    data: Literal["cvar_define"]
    data_type: str = "i64"
    variable: Sym
    size: Annotated[int, Field(gt=0)] | None


class QVarDefine(Data):
    """Defining Quantum Variables."""

    data: Literal["qvar_define"]
    data_type: str | None = "qubits"
    variable: Sym
    size: int = Field(gt=0)


class ExportVar(Data):
    """Exporting Classical Variables."""

    data: Literal["cvar_export"]
    variables: list[Sym]
    to: list[Sym] | None = None


DataMgmt: TypeAlias = CVarDefine | QVarDefine | ExportVar

# Operations


class Op(BaseModel, abc.ABC):
    """Operation Base Class."""

    model_config = ConfigDict(extra="forbid")

    metadata: dict[str, Any] | None = None


class QOp(Op):
    """Quantum operation."""

    qop: str
    returns: list[Bit] | None = None
    args: list[Bit | list[Bit]]
    angles: list[float] | None = None


class COp(Op):
    """Classical operation."""

    cop: str
    returns: list[Sym | Bit] | None = None
    args: list[int | Sym | COp | Bit]


class FFCall(COp):
    """External Classical Function Call."""

    cop: Literal["ffcall"]
    function: str


class MOp(Op):
    """Machine operation."""

    mop: str


OpType: TypeAlias = FFCall | COp | QOp | MOp


# Blocks


class Block(BaseModel, abc.ABC):
    """General block type."""

    model_config = ConfigDict(extra="forbid")

    metadata: dict[str, Any] | None = None
    block: str


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

    c: str = Field(..., alias="//", min_length=3)


class PHIRModel(BaseModel):
    """PHIR model object."""

    # Enabled for extra validation, but can change to 'allow' to preserve data
    # See https://docs.pydantic.dev/latest/concepts/models/#extra-fields
    model_config = ConfigDict(extra="forbid")

    format_: str = Field("PHIR/JSON", alias="format")
    version: str = "0.1.0"
    metadata: dict[str, Any] | None = None
    ops: list[DataMgmt | OpType | BlockType | Comment]
