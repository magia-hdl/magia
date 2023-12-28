class FixedPoint:
    def __init__(self, m: int, n: int, signed: bool = True):
        """
        Fixed point number converter
        :param m: number of integer bits
        :param n: Number of fractional bits
        :param signed: Signed or unsigned
        """
        if m < 0 or n < 0:
            raise ValueError("m and n must be positive")
        if signed and m < 1:
            raise ValueError("Signed fixed point numbers must have at least one integer bit")

        self.signed = signed
        self.m = m
        self.n = n

    def __len__(self):
        return self.width

    @property
    def width(self):
        return self.m + self.n

    @property
    def max(self):
        if self.signed:
            return (1 << (self.m - 1)) - 1 / (1 << self.n)
        return (1 << self.m) - 1 / (1 << self.n)

    @property
    def min(self):
        if not self.signed:
            return 0
        return -(1 << (self.m - 1))

    def __call__(self, value: float) -> int:
        """
        Return the fixed point representation of a float
        """
        if value > self.max:
            raise ValueError(f"Value {value} is too large for the given fixed point format")
        if value < self.min:
            raise ValueError(f"Value {value} is too small for the given fixed point format")

        scaled = value * (1 << self.n)
        # Add a small amount to avoid rounding errors
        if (scaled+0.5).is_integer():
            scaled += 0.001 if scaled > 0 else -0.001
        scaled = round(scaled)

        if not self.signed or value >= 0:
            return scaled
        return scaled & ((1 << self.width) - 1)

    def to_float(self, value: int):
        """
        Return the float representation of a fixed point number
        """
        neg = self.signed and bool(value & (1 << self.width - 1))
        if neg:
            value = (~value + 1) & ((1 << self.width) - 1)
        return value / (1 << self.n) * (-1 if neg else 1)
