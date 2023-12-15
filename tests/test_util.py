import pytest
from magia.util import sv_constant


@pytest.mark.parametrize("value, width, signed, expected", [
    (0, 8, False, "8'h00"),
    (0, 8, True, "8'h00"),
    (0xFF, 8, False, "8'hFF"),
    (-1, 8, True, "8'hFF"),
    (0x0F, 8, False, "8'h0F"),
    (0x0F, 8, True, "8'h0F"),
    (0x0F, 4, False, "4'hF"),
    (0x0F, 4, True, "4'hF"),
    (0x0F, 2, False, "2'h3"),
    (0x0F, 2, True, "2'h3"),
    (0x0F, 1, False, "1'h1"),
    (0x0F, 1, True, "1'h1"),
    (0x0F, 16, False, "16'h000F"),
    (0x0F, 16, True, "16'h000F"),
    (0x0F, 32, False, "32'h0000000F"),
    (0x0F, 32, True, "32'h0000000F"),
    (0x0F, 64, False, "64'h000000000000000F"),
    (0x0F, 64, True, "64'h000000000000000F"),
])
def test_sv_constant_integers(value, width, signed, expected):
    assert sv_constant(value, width, signed) == expected
