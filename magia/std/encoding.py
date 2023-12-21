from typing import Optional

from magia import Signal


def binary_to_onehot(binary_input: Signal, max_value: Optional[int] = None) -> Signal:
    """Converts a binary input to a one-hot output.

    Args:
        binary_input (Signal): A binary input signal.
        max_value (int, optional): The maximum value of the binary input.
          Defaults is the maximum value represented by the binary_input.

    Returns:
        Signal: A one-hot output signal.
    """
    if max_value is None:
        max_value = 2 ** len(binary_input) - 1
    if max_value >= 2 ** len(binary_input):
        raise ValueError("max_value is too large for the given binary_input")

    conversion_table = {i: 1 << i for i in range(max_value + 1)}

    return binary_input.case(conversion_table, default=0)

