"""
Core Magia package
This index shall only import modules from this level of the package.

Sub-packages (e.g. magia.std, etc.) shall be imported in their respective __init__.py files.
"""

from importlib.util import find_spec

from .bundle import Bundle, BundleSpec, BundleType
from .core import Constant, Input, Output, Register, Signal
from .memory import Memory
from .module import Blackbox, Elaborator, Instance, IOPorts, Module, VerilogWrapper

if find_spec("hdlConvertor") is not None:
    from .external import ExternalModule
else:
    # HDLConvertor is not installed. Disable ExternalModule.
    class ExternalModule:
        ERROR = NotImplementedError("ExternalModule is disabled. Install hdlConvertor to enable it.")

        def __init__(self, **kwargs):
            raise self.ERROR

        def __class_getitem__(cls, item):
            raise cls.ERROR

        @classmethod
        def from_file(cls, sv_file, top_name):
            raise cls.ERROR

        @classmethod
        def from_code(cls, sv_code, top_name):
            raise cls.ERROR

"""
Basic Signal Objects
"""
__all__ = [
    "Constant",
    "Signal",
    "Input",
    "Output",
    "Register",
]

"""
Signal Bundles
"""
__all__ += [
]

"""
Module and Instance
"""
__all__ += [
    "IOPorts",
    "Module",
    "Instance",
    "Blackbox",
    "Elaborator",
    "ExternalModule",
    "VerilogWrapper",
]

"""
Memory
"""
__all__ += [
    "Memory",
]

"""
Signal Bundles
"""
__all__ += [
    "Bundle", "BundleSpec", "BundleType",
]
