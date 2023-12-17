from math import ceil
from typing import Optional, Union


def sv_constant(value: Optional[Union[int, bytes]], width: int, signed: bool = False) -> str:
    """
    Convert a Python integer or bytes object to a SystemVerilog constant.
    If value is None, return "X", the SystemVerilog constant for an unknown value.
    """
    byte_cnt = ceil(width / 8)
    if value is not None:
        if isinstance(value, int):
            value = value.to_bytes(byte_cnt, byteorder="big", signed=signed)
        byte_mask = (2 ** width - 1).to_bytes(byte_cnt, byteorder="big")
        value = bytes([x & y for x, y in zip(value, byte_mask)])
        value = value.hex()[-(ceil(width / 4)):].upper()
    else:
        value = "X"
    sign = "s" if signed else ""
    return f"{width}'{sign}h{value}"
