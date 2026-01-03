"""
Copyright (c) Cutleast
"""

from typing import BinaryIO, Self

from pydantic import BaseModel

from .datatypes import IntegerCodec, StringCodec


class StringTable(BaseModel):
    """
    Model for string tables to look up member names and other stuff from.
    """

    count: int
    """uint16: The number of strings, this table contains."""

    strings: list[str]
    """wstring[count]: The strings."""

    @classmethod
    def parse(cls, stream: BinaryIO) -> Self:
        """
        Parses the string table from a stream of bytes.

        Args:
            stream (BinaryIO): Byte stream to read from.

        Returns:
            Self: Parsed string table.
        """

        count: int = IntegerCodec.parse(stream, IntegerCodec.IntType.UInt16)

        strings: list[str] = []
        for _ in range(count):
            strings.append(StringCodec.parse(stream, StringCodec.StrType.WString))

        return cls(count=count, strings=strings)

    def dump(self, output: BinaryIO) -> None:
        """
        Writes the string table to a stream of bytes.

        Args:
            output (BinaryIO): Byte stream to write to.

        Raises:
            ValueError: When the 'count' value does not match the actual string count.
        """

        if self.count != len(self.strings):
            raise ValueError("String table count does not match string count!")

        IntegerCodec.dump(self.count, IntegerCodec.IntType.UInt16, output)

        for string in self.strings:
            StringCodec.dump(string, StringCodec.StrType.WString, output)
