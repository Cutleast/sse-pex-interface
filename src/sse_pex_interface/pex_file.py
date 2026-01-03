"""
Copyright (c) Cutleast
"""

from typing import BinaryIO, Self

from pydantic import BaseModel

from .sections import DebugInfo, Header, StringTable


class PexFile(BaseModel):
    """
    Model for the entire PEX file.
    """

    header: Header
    """The header of the PEX file."""

    string_table: StringTable
    """The string table of the PEX file."""

    debug_info: DebugInfo
    """The debug info of the PEX file."""

    @classmethod
    def parse(cls, stream: BinaryIO) -> Self:
        """
        Parses an entire PEX file from a stream of bytes.

        Args:
            stream (BinaryIO): Byte stream to read from.

        Returns:
            Self: The parsed PEX file.
        """

        header: Header = Header.parse(stream)
        string_table: StringTable = StringTable.parse(stream)
        debug_info: DebugInfo = DebugInfo.parse(stream)

        return cls(header=header, string_table=string_table, debug_info=debug_info)

    def dump(self, output: BinaryIO) -> None:
        """
        Writes the entire PEX file to a stream of bytes.

        Args:
            output (BinaryIO): Byte stream to write to.
        """

        self.header.dump(output)
        self.string_table.dump(output)
        self.debug_info.dump(output)
