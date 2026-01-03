"""
Copyright (c) Cutleast
"""

from typing import BinaryIO, Self, override

from ..binary_model import BinaryModel
from ..datatypes import IntegerCodec
from .property import Property
from .state import State
from .variable import Variable


class ObjectData(BinaryModel):
    """
    Model for the data of an object of a PEX file.
    """

    parent_class_name: int
    """uint16: Index(base 0) into string table."""

    docstring: int
    """uint16: Index(base 0) into string table."""

    user_flags: int
    """uint32: User flags."""

    auto_state_name: int
    """uint16: Index(base 0) into string table."""

    num_variables: int
    """uint16: Number of variables."""

    variables: list[Variable]
    """List of variables."""

    num_properties: int
    """uint16: Number of properties."""

    properties: list[Property]
    """List of properties."""

    num_states: int
    """uint16: Number of states."""

    states: list[State]
    """List of states."""

    @override
    @classmethod
    def parse(cls, stream: BinaryIO) -> Self:
        parent_class_name: int = IntegerCodec.parse(stream, IntegerCodec.IntType.UInt16)
        docstring: int = IntegerCodec.parse(stream, IntegerCodec.IntType.UInt16)
        user_flags: int = IntegerCodec.parse(stream, IntegerCodec.IntType.UInt32)
        auto_state_name: int = IntegerCodec.parse(stream, IntegerCodec.IntType.UInt16)

        num_variables: int = IntegerCodec.parse(stream, IntegerCodec.IntType.UInt16)
        variables: list[Variable] = []
        for _ in range(num_variables):
            variables.append(Variable.parse(stream))

        num_properties: int = IntegerCodec.parse(stream, IntegerCodec.IntType.UInt16)
        properties: list[Property] = []
        for _ in range(num_properties):
            properties.append(Property.parse(stream))

        num_states: int = IntegerCodec.parse(stream, IntegerCodec.IntType.UInt16)
        states: list[State] = []
        for _ in range(num_states):
            states.append(State.parse(stream))

        return cls(
            parent_class_name=parent_class_name,
            docstring=docstring,
            user_flags=user_flags,
            auto_state_name=auto_state_name,
            num_variables=num_variables,
            variables=variables,
            num_properties=num_properties,
            properties=properties,
            num_states=num_states,
            states=states,
        )

    @override
    def dump(self, output: BinaryIO) -> None:
        if len(self.variables) != self.num_variables:
            raise ValueError(
                "Value of 'num_variables' does not match actual variable count!"
            )

        if len(self.properties) != self.num_properties:
            raise ValueError(
                "Value of 'num_properties' does not match actual property count!"
            )

        if len(self.states) != self.num_states:
            raise ValueError("Value of 'num_states' does not match actual state count!")

        IntegerCodec.dump(self.parent_class_name, IntegerCodec.IntType.UInt16, output)
        IntegerCodec.dump(self.docstring, IntegerCodec.IntType.UInt16, output)
        IntegerCodec.dump(self.user_flags, IntegerCodec.IntType.UInt32, output)
        IntegerCodec.dump(self.auto_state_name, IntegerCodec.IntType.UInt16, output)

        IntegerCodec.dump(self.num_variables, IntegerCodec.IntType.UInt16, output)

        for variable in self.variables:
            variable.dump(output)

        IntegerCodec.dump(self.num_properties, IntegerCodec.IntType.UInt16, output)

        for property in self.properties:
            property.dump(output)

        IntegerCodec.dump(self.num_states, IntegerCodec.IntType.UInt16, output)

        for state in self.states:
            state.dump(output)
