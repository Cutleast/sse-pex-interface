"""
Copyright (c) Cutleast
"""

from typing import BinaryIO, Self, override

from ..binary_model import BinaryModel
from ..datatypes import IntegerCodec
from .named_function import NamedFunction


class State(BinaryModel):
    """
    Model for a state of a PEX file.
    """

    name: int
    """uint16: Index(base 0) into string table, empty string for default state."""

    num_functions: int
    """uint16: Number of functions in this state."""

    functions: list[NamedFunction]
    """List of functions in this state."""

    @override
    @classmethod
    def parse(cls, stream: BinaryIO) -> Self:
        name: int = IntegerCodec.parse(stream, IntegerCodec.IntType.UInt16)
        num_functions: int = IntegerCodec.parse(stream, IntegerCodec.IntType.UInt16)

        functions: list[NamedFunction] = []
        for _ in range(num_functions):
            functions.append(NamedFunction.parse(stream))

        return cls(name=name, num_functions=num_functions, functions=functions)

    @override
    def dump(self, output: BinaryIO) -> None:
        if len(self.functions) != self.num_functions:
            raise ValueError(
                "Value of 'num_functions' does not match actual function count!"
            )

        IntegerCodec.dump(self.name, IntegerCodec.IntType.UInt16, output)
        IntegerCodec.dump(self.num_functions, IntegerCodec.IntType.UInt16, output)

        for function in self.functions:
            function.dump(output)
