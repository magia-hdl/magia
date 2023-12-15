from math import ceil
from typing import Union


def sv_constant(value: Union[int, bytes], width: int, signed: bool = False) -> str:
    byte_cnt = ceil(width / 8)
    if isinstance(value, int):
        value = value.to_bytes(byte_cnt, byteorder="big", signed=signed)
    byte_mask = (2 ** width - 1).to_bytes(byte_cnt, byteorder="big")
    value = bytes([x & y for x, y in zip(value, byte_mask)])
    return f"{width}'h{value.hex()[-(ceil(width / 4)):].upper()}"
