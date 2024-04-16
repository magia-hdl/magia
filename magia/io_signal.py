from __future__ import annotations

from typing import TYPE_CHECKING

from .core import Signal
from .data_struct import SignalType

if TYPE_CHECKING:
    from .module import Instance


class Input(Signal):
    """
    Representing an input signal.

    It has no driver, but it is driving other signals.
    It is used by both the module declaration and the module instance.
    """

    def __init__(
            self,
            name: str, width: int, signed: bool = False,
            owner_instance: Instance | None = None,
            **kwargs
    ):
        """I/O ports must have name and width well-defined by designers."""
        if name is None:
            raise ValueError("Input name is not set")
        if width == 0:
            raise ValueError("Input width is not set")

        super().__init__(name=name, width=width, signed=signed, **kwargs)
        self._config.signal_type = SignalType.INPUT
        self._config.owner_instance = owner_instance

    def elaborate(self) -> str:
        """
        Elaborate the input signal in the module declaration.

        :returns: input logic (signed) [...]PORT_NAME.
        """
        port_decl = self.signal_decl().rstrip(";")
        return f"input  {port_decl}"


class Output(Signal):
    """
    Representing an output signal.

    They are the starting points when we elaborate the module.
    It is used by both the module declaration and the module instance.
    """

    def __init__(
            self,
            name: str, width: int, signed: bool = False,
            owner_instance: Instance | None = None,
            **kwargs
    ):
        """I/O ports must have name and width well-defined by designers."""
        if name is None:
            raise ValueError("Output name is not set")
        if width == 0:
            raise ValueError("Output width is not set")
        super().__init__(name=name, width=width, signed=signed, **kwargs)
        self._config.signal_type = SignalType.OUTPUT
        self._config.owner_instance = owner_instance

    def elaborate(self) -> str:
        """
        Elaborate the output signal in the module declaration.

        :returns: output logic (signed) [...]PORT_NAME.
        """
        port_decl = self.signal_decl().rstrip(";")
        return f"output {port_decl}"
