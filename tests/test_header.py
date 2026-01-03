"""
Copyright (c) Cutleast
"""

from io import BytesIO
from pathlib import Path
from typing import BinaryIO

from sse_pex_interface.header import Header


class TestHeader:
    """
    Tests reading and writing of the header section of a PEX file.
    """

    def test_parse_header(self) -> None:
        """
        Tests parsing the header section of a PEX file.
        """

        # given
        pex_file: Path = Path.cwd() / "tests" / "test_data" / "_wetquestscript.pex"

        # when
        with pex_file.open("rb") as stream:
            header: Header = Header.parse(stream)

        # then
        assert header.magic == 0xFA57C0DE
        assert header.major_version == 3
        assert header.minor_version == 2
        assert header.game_id == 1
        assert header.compilation_time == 1601329996
        assert header.source_file_name == "_WetQuestScript.psc"
        assert header.username == "TechAngel"
        assert header.machinename == "DESKTOP-O95F7AQ"

    def test_dump_header(self) -> None:
        """
        Tests writing the header section of a PEX file.
        """

        # given
        pex_file: Path = Path.cwd() / "tests" / "test_data" / "_wetquestscript.pex"
        output: BinaryIO = BytesIO()
        with pex_file.open("rb") as stream:
            header: Header = Header.parse(stream)

        # when
        header.dump(output)
        output.seek(0)
        dumped_header: Header = Header.parse(output)

        # then
        assert header == dumped_header
