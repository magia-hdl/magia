from contextlib import contextmanager
from tempfile import NamedTemporaryFile

from magia import Elaborator, Module


@contextmanager
def elaborate_to_file(module: Module) -> str:
    with NamedTemporaryFile(mode="w", suffix=".sv") as f:
        f.write(Elaborator.to_string(module))
        f.flush()
        yield f.name
