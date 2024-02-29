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
    data_type: Literal["i64", "i32", "u64", "u32"]
    variable: Sym
    size: PositiveInt | None

    @model_validator(mode="after")
    def check_size(self: CVarDefine) -> CVarDefine:
        """Checks whether size fits the data_type."""
        msg = "`size` is greater than what `data_type` can handle"
        if self.size:
            match self.data_type:
                case "i64" | "u64":
                    if self.size > 64:  # noqa: PLR2004
                        raise ValueError(msg)
                case "i32" | "u32":
                    if self.size > 32:  # noqa: PLR2004
                        raise ValueError(msg)
        return self


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

# Meta Instructions


class Meta(BaseModel, abc.ABC):
    """Meta instructions base class."""

    model_config = ConfigDict(extra="forbid")

    meta: str


class Barrier(Meta):
    """Barrier instruction."""

    meta: Literal["barrier"]
    args: list[Bit]


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
        "R2XXYYZZ",
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
                    msg = f"{self.qop} gate requires exactly one angle parameter."
                    raise ValueError(msg)
            case "R2XXYYZZ":
                if not self.angles or len(self.angles[0]) != 3:  # noqa: PLR2004
                    msg = f"{self.qop} gate requires three angle parameters."
                    raise ValueError(msg)
            case _:
                if self.angles:
                    msg = "This gate takes no angles."
                    raise ValueError(msg)
        return self


QOp: TypeAlias = MeasOp | SQOp | TQOp

# Classical Operations


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


# Machine Operations

Duration = NewType("Duration", tuple[float, Literal["s", "ms", "us", "ns"]])


class MOp(Op, abc.ABC):
    """Machine operation."""

    model_config = ConfigDict(extra="forbid")

    mop: str
    args: list[Bit] | None = None
    duration: Duration | None = None


class IdleMOp(MOp):
    """Idle machine op."""

    mop: Literal["Idle"]
    args: list[Bit]
    duration: Duration


class TransportMOp(MOp):
    """Transport machine op."""

    mop: Literal["Transport"]
    duration: Duration


class SkipMOp(MOp):
    """Skip machine op."""

    mop: Literal["Skip"]


MOpType: TypeAlias = IdleMOp | TransportMOp | SkipMOp
OpType: TypeAlias = FFCall | COp | QOp | MOpType | Barrier


# Blocks


class Block(BaseModel, abc.ABC):
    """Base class for block type."""

    model_config = ConfigDict(extra="forbid")

    metadata: dict[str, Any] | None = None
    block: str


class SeqBlock(Block):
    """A generic sequence block."""

    block: Literal["sequence"]
    ops: list[OpType | BlockType]


class QParBlock(Block):
    """Parallel quantum operations block."""

    block: Literal["qparallel"]
    ops: list[QOp]


class IfBlock(Block):
    """If/else block."""

    block: Literal["if"]
    condition: COp
    true_branch: list[OpType | BlockType]
    false_branch: list[OpType | BlockType] | None = None


BlockType: TypeAlias = SeqBlock | QParBlock | IfBlock


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
