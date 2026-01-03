"""
Copyright (c) Cutleast
"""

from io import BytesIO
from pathlib import Path
from typing import BinaryIO

from sse_pex_interface.header import Header
from sse_pex_interface.string_table import StringTable


class TestStringTable:
    """
    Tests reading and writing the string table of a PEX file.
    """

    def test_parse(self) -> None:
        """
        Tests parsing the string table of a PEX file.
        """

        # given
        pex_file_path: Path = Path.cwd() / "tests" / "test_data" / "_wetquestscript.pex"

        # when
        with pex_file_path.open("rb") as stream:
            Header.parse(stream)  # skip header
            string_table: StringTable = StringTable.parse(stream)

        # then
        assert string_table.count == 624
        assert string_table.strings[:5] == [
            "_wetquestscript",
            "",
            "GetState",
            "GotoState",
            "ScanArea",
        ]

    def test_dump(self) -> None:
        """
        Tests writing a string table.
        """

        # given
        pex_file_path: Path = Path.cwd() / "tests" / "test_data" / "_wetquestscript.pex"
        output: BinaryIO = BytesIO()
        with pex_file_path.open("rb") as stream:
            Header.parse(stream)  # skip header
            string_table: StringTable = StringTable.parse(stream)

        # when
        string_table.dump(output)
        output.seek(0)
        dumped_string_table: StringTable = StringTable.parse(output)

        # then
        assert string_table == dumped_string_table
