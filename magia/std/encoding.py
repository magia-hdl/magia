from typing import Optional

from magia import Signal, Constant


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
    signal_width = max_value + 1
    if max_value >= 2 ** len(binary_input):
        raise ValueError("max_value is too large for the given binary_input")

    conversion_table = {i: 1 << i for i in range(max_value + 1)}

    return binary_input.case(conversion_table, default=0).with_width(signal_width)


def onehot_to_binary(onehot_input: Signal) -> Signal:
    """Converts a one-hot input to a binary output.

    Args:
        onehot_input (Signal): A one_hot input signal.

    Returns:
        Signal: A binary output signal.
    """
    binary_width = (len(onehot_input)-1).bit_length()
    conversion_table = [
        Constant(i, binary_width).when(onehot_input[i])
        for i in range(len(onehot_input))
    ]
    binary_out = Constant(0, binary_width)
    for entry in conversion_table:
        binary_out |= entry
    return binary_out

