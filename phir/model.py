##############################################################################
#
# Copyright (c) 2023 Quantinuum LLC All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
#
##############################################################################

"""PHIR model lives here."""

from __future__ import annotations

import abc
from typing import Any, Literal, NewType, TypeAlias

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    NonNegativeInt,
    PositiveInt,
    model_validator,
)

Sym: TypeAlias = str
Idx = NewType("Idx", NonNegativeInt)
Bit = NewType("Bit", tuple[Sym, Idx])

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
    size: PositiveInt | None


class QVarDefine(Data):
    """Defining Quantum Variables."""

    data: Literal["qvar_define"]
    data_type: str | None = "qubits"
    variable: Sym
    size: PositiveInt


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


class MeasOp(Op):
    """Measurement operation."""

    qop: Literal["Measure"]
    returns: list[Bit]
    args: list[Bit]

    @model_validator(mode="after")
    def check_sizes(self: MeasOp) -> MeasOp:
        """Checks whether returns and args lengths match."""
        msg = "Lengths of `returns` and `args` do not match."
        if len(self.returns) != len(self.args):
            raise ValueError(msg)
        return self


class SQOp(Op):
    """Single-qubit Quantum operation."""

    # From https://github.com/CQCL/phir/blob/main/spec.md#table-ii---quantum-operations
    qop: Literal[
        "Init",
        "I",
        "X",
        "Y",
        "Z",
        "RX",
        "RY",
        "RZ",
        "R1XY",
        "SX",
        "SXdg",
        "SY",
        "SYdg",
        "SZ",
        "SZdg",
        "H",
        "F",
        "Fdg",
        "T",
        "Tdg",
    ]
    angles: tuple[list[float], Literal["rad", "pi"]] | None = None
    args: list[Bit]

    @model_validator(mode="after")
    def check_angles(self: SQOp) -> SQOp:
        """Checks whether correct number of angles are provided for a given gate."""
        msg = "Incorrect number of angles for the given gate."
        match self.qop:
            case "R1XY":
                if not self.angles or len(self.angles[0]) != 2:  # noqa: PLR2004
                    raise ValueError(msg)
            case "RX" | "RY" | "RZ":
                if not self.angles or len(self.angles[0]) != 1:
                    raise ValueError(msg)
            case _:
                if self.angles:
                    msg = "This gate takes no angles."
                    raise ValueError(msg)
        return self


class TQOp(Op):
    """Two-qubit Quantum operation."""

    # From https://github.com/CQCL/phir/blob/main/spec.md#table-ii---quantum-operations
    qop: Literal[
        "CX",
        "CY",
        "CZ",
        "RXX",
        "RYY",
        "RZZ",
        "SXX",
        "SXXdg",
        "SYY",
        "SYYdg",
        "SZZ",
        "SZZdg",
        "SWAP",
    ]
    angles: tuple[list[float], Literal["rad", "pi"]] | None = None
    args: list[tuple[Bit, Bit]]

    @model_validator(mode="after")
    def check_angles(self: TQOp) -> TQOp:
        """Checks whether correct number of angles are provided for a given gate."""
        match self.qop:
            case "RXX" | "RYY" | "RZZ":
                if not self.angles or len(self.angles[0]) != 1:
                    msg = "Incorrect number of angles for the given gate."
                    raise ValueError(msg)
            case _:
                if self.angles:
                    msg = "This gate takes no angles."
                    raise ValueError(msg)
        return self


class ThreeQOp(Op):
    """Three-qubit Quantum operation."""

    # From https://github.com/CQCL/phir/blob/main/spec.md#table-ii---quantum-operations
    # Note: args and angles are specialized for the needs of R2XXYYZZ
    qop: Literal["R2XXYYZZ"]
    angles: tuple[tuple[float], Literal["rad", "pi"]]
    args: list[tuple[Bit, Bit, Bit]]


class COp(Op):
    """Classical operation."""

    # From https://github.com/CQCL/phir/blob/main/spec.md#table-i---cop-assignment-arithmetic-comparison--bitwise-operations
    cop: Literal[
        "=",
        "+",
        "-",
        "*",
        "/",
        "%",
        "==",
        "!=",
        ">",
        "<",
        ">=",
        "<=",
        "&",
        "|",
        "^",
        "~",
        "<<",
        ">>",
    ]
    returns: list[Sym | Bit] | None = None
    args: list[int | Sym | COp | Bit]


class FFCall(Op):
    """(Classical) Foreign Function Call."""

    cop: Literal["ffcall"]
    returns: list[Sym | Bit] | None = None
    function: str
    args: list[int | Sym | COp | Bit]


Duration = NewType("Duration", tuple[float, Literal["s", "ms", "us", "ns"]])


class MOp(Op):
    """Machine operation."""

    mop: str
    duration: Duration | None = None


QOp: TypeAlias = MeasOp | SQOp | TQOp | ThreeQOp
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

# Comments


class Comment(BaseModel):
    """Optional comment."""

    model_config = ConfigDict(extra="forbid")

    c: str = Field(..., alias="//", min_length=3)


Cmd: TypeAlias = DataMgmt | OpType | BlockType | Comment


class PHIRModel(BaseModel):
    """PHIR model object."""

    # Enabled for extra validation, but can change to 'allow' to preserve data
    # See https://docs.pydantic.dev/latest/concepts/models/#extra-fields
    model_config = ConfigDict(extra="forbid")

    format_: str = Field("PHIR/JSON", alias="format")
    version: str = "0.1.0"
    metadata: dict[str, Any] | None = None
    ops: list[Cmd]


COp.model_rebuild()  # type: ignore [misc]
SeqBlock.model_rebuild()  # type: ignore [misc]
