from enum import Enum, IntEnum, auto


class SignalType(Enum):
    """
    Kinds of signals
    """
    WIRE = 0
    INPUT = 1
    OUTPUT = 2
    MEMORY = 3
    CONSTANT = 4


class OPType(IntEnum):
    """
    List of operations that can be performed on signals
    """
    ANY = auto()
    ALL = auto()
    PARITY = auto()

    NOT = auto()
    OR = auto()
    AND = auto()
    XOR = auto()
    LSHIFT = auto()
    RSHIFT = auto()
    ALSHIFT = auto()
    ARSHIFT = auto()
    ADD = auto()
    MINUS = auto()
    MUL = auto()
    EQ = auto()
    NEQ = auto()
    LT = auto()
    LE = auto()
    GT = auto()
    GE = auto()

    SLICE = auto()
    CONCAT = auto()

    REG = auto()
    WHEN = auto()
    CASE = auto()
    MUX = auto()


class RegType(IntEnum):
    DFF = auto()
    DFF_EN = auto()
    DFF_RST = auto()
    DFF_EN_RST = auto()
    DFF_ASYNC_RST = auto()
    DFF_EN_ASYNC_RST = auto()
    DFF_BOTH_RST = auto()
    DFF_EN_BOTH_RST = auto()
