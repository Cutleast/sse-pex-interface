"""
Copyright (c) Cutleast
"""

from typing import BinaryIO, Self, override

from .binary_model import BinaryModel
from .datatypes import IntegerCodec
from .sections import DebugInfo, Header, StringTable, UserFlag


class PexFile(BinaryModel):
    """
    Model for the entire PEX file.
    """

    header: Header
    """The header of the PEX file."""

    string_table: StringTable
    """The string table of the PEX file."""

    debug_info: DebugInfo
    """The debug info of the PEX file."""

    user_flag_count: int
    """uint16: The number of user flags in the PEX file."""

    user_flags: list[UserFlag]
    """The user flags of the PEX file."""

    @override
    @classmethod
    def parse(cls, stream: BinaryIO) -> Self:
        header: Header = Header.parse(stream)
        string_table: StringTable = StringTable.parse(stream)
        debug_info: DebugInfo = DebugInfo.parse(stream)
        user_flag_count: int = IntegerCodec.parse(stream, IntegerCodec.IntType.UInt16)

        user_flags: list[UserFlag] = []
        for _ in range(user_flag_count):
            user_flags.append(UserFlag.parse(stream))

        return cls(
            header=header,
            string_table=string_table,
            debug_info=debug_info,
            user_flag_count=user_flag_count,
            user_flags=user_flags,
        )

    @override
    def dump(self, output: BinaryIO) -> None:
        if len(self.user_flags) != self.user_flag_count:
            raise ValueError(
                "Value of `user_flag_count` does not match actual user flag count!"
            )

        self.header.dump(output)
        self.string_table.dump(output)
        self.debug_info.dump(output)

        IntegerCodec.dump(self.user_flag_count, IntegerCodec.IntType.UInt16, output)

        for user_flag in self.user_flags:
            user_flag.dump(output)
