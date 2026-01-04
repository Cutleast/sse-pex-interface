"""
Copyright (c) Cutleast
"""

import pytest

from sse_pex_interface.sections import VariableData


class TestVariableData:
    """
    Tests for the VariableData model.
    """

    def test_validation_on_init(self) -> None:
        """
        Tests the correct validation of the model's data on initialization.
        """

        # when/then
        with pytest.raises(TypeError):
            VariableData(type=VariableData.Type.NULL, data=2, integer_unsigned=False)

        # when/then
        with pytest.raises(TypeError):
            VariableData(
                type=VariableData.Type.INTEGER, data=None, integer_unsigned=False
            )

    def test_validation_on_mutation(self) -> None:
        """
        Tests the correct validation of the model's data when a value is changed.
        """

        # given
        variable_data = VariableData(
            type=VariableData.Type.NULL, data=None, integer_unsigned=False
        )

        # when/then
        with pytest.raises(TypeError):
            variable_data.data = 2
