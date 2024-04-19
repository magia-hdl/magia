from magia import Constant, Signal


def binary_to_onehot(binary_input: Signal, max_value: None | int = None) -> Signal:
    """
    Convert a binary input to a one-hot output.

    :param binary_input: A binary input signal.
    :param max_value: The maximum value of the binary input.
        Defaults is the maximum value represented by the binary_input.
    :returns: A one-hot output signal.
    """
    if max_value is None:
        max_value = 2 ** binary_input.width - 1
    if max_value >= 2 ** binary_input.width:
        raise ValueError("max_value is too large for the given binary_input")

    conversion_table = {i: 1 << i for i in range(max_value + 1)}

    return binary_input.case(conversion_table, default=0)


def onehot_to_binary(onehot_input: Signal) -> Signal:
    """
    Convert a one-hot input to a binary output.

    :param onehot_input: A one-hot input signal.
    :returns: A binary output signal.
    """
    binary_width = (onehot_input.width - 1).bit_length()
    conversion_table = [
        Constant(i, binary_width).when(onehot_input[i])
        for i in range(onehot_input.width)
    ]
    binary_out = Constant(0, binary_width)
    for entry in conversion_table:
        binary_out |= entry
    return binary_out
