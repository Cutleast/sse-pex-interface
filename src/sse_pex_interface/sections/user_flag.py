"""
Copyright (c) Cutleast
"""

from typing import BinaryIO, Self

from pydantic import BaseModel

from ..datatypes import IntegerCodec


class UserFlag(BaseModel):
    """
    Model representing a user flag of a PEX file.
    """

    name_index: int
    """uint16: Index(base 0) into string table."""

    flag_index: int
    """uint8: Bit index."""

    @classmethod
    def parse(cls, stream: BinaryIO) -> Self:
        """
        Parses a user flag from a stream of bytes.

        Args:
            stream (BinaryIO): Byte stream to read from.

        Returns:
            Self: The parsed user flag.
        """

        name_index: int = IntegerCodec.parse(stream, IntegerCodec.IntType.UInt16)
        flag_index: int = IntegerCodec.parse(stream, IntegerCodec.IntType.UInt8)

        return cls(name_index=name_index, flag_index=flag_index)

    def dump(self, output: BinaryIO) -> None:
        """
        Writes the user flag to a stream of bytes.

        Args:
            output (BinaryIO): Byte stream to write to.
        """

        IntegerCodec.dump(self.name_index, IntegerCodec.IntType.UInt16, output)
        IntegerCodec.dump(self.flag_index, IntegerCodec.IntType.UInt8, output)
