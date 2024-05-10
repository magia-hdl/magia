from __future__ import annotations

from typing import TYPE_CHECKING

from .data_struct import SignalType
from .factory import signal_config_like
from .signals import Signal

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
            owner_instance: None | Instance = None,
            **kwargs
    ):
        """I/O ports must have name and width well-defined by designers."""
        if name is None:
            raise ValueError("Input name is not set")
        if width == 0:
            raise ValueError("Input width is not set")

        super().__init__(name=name, width=width, signed=signed, **kwargs)
        self.signal_config.signal_type = SignalType.INPUT
        self.signal_config.owner_instance = owner_instance

    @property
    def is_input(self) -> bool:
        """Check if the signal is an input signal."""
        return True

    def elaborate(self) -> str:
        """
        Elaborate the input signal in the module declaration.

        :returns: input logic (signed) [...]PORT_NAME.
        """
        port_decl = self.signal_decl().rstrip(";")
        return f"input  {port_decl}"

    def __ilshift__(self, other):
        if self.owner_instance is None:
            raise ValueError("Cannot drive the Input of a module type.")
        return super().__ilshift__(other)

    @classmethod
    def like(cls, signal: Signal, **kwargs) -> Signal:
        """Create an Input with the same configuration as the given signal."""
        return Input(**signal_config_like(signal, **kwargs))


class Output(Signal):
    """
    Representing an output signal.

    They are the starting points when we elaborate the module.
    It is used by both the module declaration and the module instance.
    """

    def __init__(
            self,
            name: str, width: int, signed: bool = False,
            owner_instance: None | Instance = None,
            **kwargs
    ):
        """I/O ports must have name and width well-defined by designers."""
        if name is None:
            raise ValueError("Output name is not set")
        if width == 0:
            raise ValueError("Output width is not set")
        super().__init__(name=name, width=width, signed=signed, **kwargs)
        self.signal_config.signal_type = SignalType.OUTPUT
        self.signal_config.owner_instance = owner_instance

    @property
    def is_output(self) -> bool:
        """Check if the signal is an output signal."""
        return True

    def elaborate(self) -> str:
        """
        Elaborate the output signal in the module declaration.

        :returns: output logic (signed) [...]PORT_NAME.
        """
        port_decl = self.signal_decl().rstrip(";")
        return f"output {port_decl}"

    def __ilshift__(self, other):
        if self.owner_instance is not None:
            raise ValueError("Cannot drive output of a module instance.")
        return super().__ilshift__(other)

    @classmethod
    def like(cls, signal: Signal, **kwargs) -> Signal:
        """Create an output with the same configuration as the given signal."""
        return Output(**signal_config_like(signal, **kwargs))
