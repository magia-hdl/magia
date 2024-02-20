import pytest

from magia.format import FixedPoint


class TestFixedPoint:
    def test_overflow_assertion_signed(self):
        fp4_4 = FixedPoint(4, 4)
        for i in [16, 8, -8.5, fp4_4.max + 0.001, fp4_4.min - 0.001]:
            with pytest.raises(ValueError):
                fp4_4(i)
        for i in [2, -3, 0, -8, 7.9375, -7.9375]:
            fp4_4(i)

    def test_overflow_assertion_unsigned(self):
        fp4_4 = FixedPoint(4, 4, signed=False)
        for i in [32, 16, -1, -17, fp4_4.max + 0.001, -1 / (1 << 5)]:
            with pytest.raises(ValueError):
                fp4_4(i)
        for i in [2, 0, 15, fp4_4.max]:
            fp4_4(i)

    @pytest.mark.parametrize("m,n,range_max,range_min", [
        (4, 4, 8 - 1 / 16, -8),
        (4, 3, 8 - 1 / 8, -8),
        (4, 2, 8 - 1 / 4, -8),
        (4, 1, 8 - 1 / 2, -8),
        (4, 0, 7, -8),
        (3, 4, 4 - 1 / 16, -4),
        (2, 4, 2 - 1 / 16, -2),
        (1, 4, 1 - 1 / 16, -1),
    ])
    def test_signed_range(self, m, n, range_max, range_min):
        fp_fmt = FixedPoint(m, n, signed=True)
        assert fp_fmt.max == range_max
        assert fp_fmt.min == range_min

    @pytest.mark.parametrize("m,n,range_max,range_min", [
        (4, 4, 16 - 1 / 16, 0),
        (4, 3, 16 - 1 / 8, 0),
        (4, 2, 16 - 1 / 4, 0),
        (4, 1, 16 - 1 / 2, 0),
        (4, 0, 15, 0),
        (3, 4, 8 - 1 / 16, 0),
        (2, 4, 4 - 1 / 16, 0),
        (1, 4, 2 - 1 / 16, 0),
        (0, 4, 1 - 1 / 16, 0),
    ])
    def test_unsigned_range(self, m, n, range_max, range_min):
        fp_fmt = FixedPoint(m, n, signed=False)
        assert fp_fmt.max == range_max
        assert fp_fmt.min == range_min

    @pytest.mark.parametrize("m,n,src,expected", [
        (4, 4, 0.0, 0b00000000),
        (4, 4, 0.5, 0b00001000),
        (4, 4, 0.25, 0b00000100),
        (4, 4, 0.875, 0b00001110),
        (4, 4, 0.0625, 0b00000001),
        (4, 4, 0.9375, 0b00001111),
        (4, 4, 7.9375, 0b01111111),
        (4, 4, 15.0, 0b11110000),
        (4, 4, 15.9375, 0b11111111),
        (3, 2, 0.0, 0b00000),
        (3, 2, 0.5, 0b00010),
        (3, 2, 0.25, 0b00001),
        (3, 2, 7.0, 0b11100),
        (3, 2, 7.75, 0b11111),
        (0, 2, 0.0, 0b00),
        (0, 2, 0.5, 0b10),
        (0, 2, 0.25, 0b01),
    ])
    def test_unsigned_conversion(self, m, n, src, expected):
        fp_fmt = FixedPoint(m, n, signed=False)
        assert fp_fmt(src) == expected

    @pytest.mark.parametrize("m,n,src,expected", [
        (4, 4, 0.0, 0b00000000),
        (4, 4, 0.5, 0b00001000),
        (4, 4, 0.25, 0b00000100),
        (4, 4, 0.875, 0b00001110),
        (4, 4, 0.0625, 0b00000001),
        (4, 4, 0.9375, 0b00001111),
        (4, 4, 7.9375, 0b01111111),
        (4, 4, -8.0, 0b10000000),
        (4, 4, -7.9375, 0b10000001),
        (4, 4, -0.0625, 0b11111111),
        (4, 4, -0.9375, 0b11110001),
        (3, 2, 0.0, 0b00000),
        (3, 2, 0.5, 0b00010),
        (3, 2, 0.25, 0b00001),
        (3, 2, -0.25, 0b11111),
        (3, 2, -0.5, 0b11110),
        (3, 2, 3.75, 0b01111),
        (3, 2, -4.0, 0b10000),
        (3, 2, -3.75, 0b10001),
        (1, 1, 0.0, 0b00),
        (1, 1, 0.5, 0b01),
        (1, 1, -0.5, 0b11),
        (1, 1, -1.0, 0b10),
    ])
    def test_signed_conversion(self, m, n, src, expected):
        fp_fmt = FixedPoint(m, n, signed=True)
        assert fp_fmt(src) == expected

    @pytest.mark.parametrize("m,n,signed", [
        (8, 4, False),
        (4, 4, False),
        (4, 3, False),
        (4, 2, False),
        (4, 1, False),
        (4, 0, False),
        (3, 4, False),
        (2, 4, False),
        (1, 4, False),
        (0, 4, False),
        (8, 4, True),
        (4, 4, True),
        (4, 3, True),
        (4, 2, True),
        (4, 1, True),
        (4, 0, True),
        (3, 4, True),
        (2, 4, True),
        (1, 4, True),
    ])
    def test_back_conversion(self, m, n, signed):
        fp_fmt = FixedPoint(m, n, signed=signed)
        for i in range(1 << len(fp_fmt)):
            src = fp_fmt.min + i / (1 << n)
            result = fp_fmt.to_float(fp_fmt(src))
            assert result == src, f"Expect {src}, got {result}"

    @pytest.mark.parametrize("src, expected", [
        (0.0, 0b000000),
        (0.124, 0b000000),
        (0.125, 0b000001),
        (0.126, 0b000001),
        (0.51, 0b000010),
        (0.50 + 0.124, 0b000010),
        (0.50 + 0.125, 0b000011),
        (0.50 + 0.126, 0b000011),
        (-0.124, 0b000000),
        (-0.125, 0b111111),
        (-0.126, 0b111111),
        (-0.250 + 0.001, 0b111111),
        (-0.50 - 0.124, 0b111110),
        (-0.50 - 0.125, 0b111101),
        (-0.50 - 0.126, 0b111101),
    ])
    def test_rounding(self, src, expected):
        """
        Rounding occur at LSB/2. Different from Python's round() function.
        """
        fp_fmt = FixedPoint(4, 2, signed=True)
        assert fp_fmt(src) == expected

    def test_width(self):
        fp_fmt = FixedPoint(4, 4)
        assert len(fp_fmt) == 8
