import pytest
import sys

from contextlib import contextmanager
from tempfile import NamedTemporaryFile

from magia import Module


@contextmanager
def elaborate_to_file(module: Module) -> str:
    sv_code = Module.elaborate_all(module)
    sv_code = "\n".join(sv_code.values())

    with NamedTemporaryFile(mode="w", suffix=".sv") as f:
        f.write(sv_code)
        f.flush()
        yield f.name


sys.modules['pytest'].elaborate_to_file = elaborate_to_file
