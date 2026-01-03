"""
Copyright (c) Cutleast
"""

from typing import BinaryIO, Self, override

from ..binary_model import BinaryModel
from ..datatypes import IntegerCodec, StringCodec


class StringTable(BinaryModel):
    """
    Model for string tables to look up member names and other stuff from.
    """

    count: int
    """uint16: The number of strings, this table contains."""

    strings: list[str]
    """wstring[count]: The strings."""

    @override
    @classmethod
    def parse(cls, stream: BinaryIO) -> Self:
        count: int = IntegerCodec.parse(stream, IntegerCodec.IntType.UInt16)

        strings: list[str] = []
        for _ in range(count):
            strings.append(StringCodec.parse(stream, StringCodec.StrType.WString))

        return cls(count=count, strings=strings)

    @override
    def dump(self, output: BinaryIO) -> None:
        if self.count != len(self.strings):
            raise ValueError("String table count does not match string count!")

        IntegerCodec.dump(self.count, IntegerCodec.IntType.UInt16, output)

        for string in self.strings:
            StringCodec.dump(string, StringCodec.StrType.WString, output)
