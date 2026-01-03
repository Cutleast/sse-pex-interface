"""
Copyright (c) Cutleast
"""

from abc import ABC, abstractmethod
from typing import BinaryIO, Self

from pydantic import BaseModel


class BinaryModel(BaseModel, ABC):
    """
    Abstract base class for all models that can be deserialized from and serialized to
    binary.
    """

    @classmethod
    @abstractmethod
    def parse(cls, stream: BinaryIO) -> Self:
        """
        Parses the model from a stream of bytes.

        Args:
            stream (BinaryIO): Byte stream to read from.

        Returns:
            Self: The parsed model.
        """

    @abstractmethod
    def dump(self, output: BinaryIO) -> None:
        """
        Writes the model's data to a stream of bytes.

        Args:
            output (BinaryIO): Byte stream to write to.
        """
