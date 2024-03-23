from typing import Optional

from magia import Signal


def edge_detector(
        signal: Signal, clk: Signal,
        reset: Optional[Signal] = None, async_reset: Optional[Signal] = None,
        edge: str = "rising", registered: bool = True,
) -> Signal:
    """Detects the given edge of the input signal.

    :param signal: The input signal.
    :param clk: The clock signal.
    :param reset: The reset signal.
    :param async_reset: The async reset signal.
    :param edge: The edge to detect, "rising", "falling" or "both". Default is "rising".
    :param registered: Register the output signal. Default is True.

    :return: The detected edge signal.
    """
    if reset is None and async_reset is None:
        raise ValueError("reset or async_reset must be provided")
    if edge not in ("rising", "falling", "both"):
        raise ValueError('edge must be "rising", "falling" or "both"')
    if len(signal) != 1:
        raise ValueError("signal must be a single bit")
    resets = {
        "reset": reset, "async_reset": async_reset,
        "reset_value": 0, "async_reset_value": 0
    }

    prev = signal.reg(clk, **resets)
    edge_detected = {
        "rising": signal & ~prev,
        "falling": ~signal & prev,
        "both": signal ^ prev,
    }[edge]

    if registered:
        edge_detected = edge_detected.reg(clk, **resets)
    return edge_detected
