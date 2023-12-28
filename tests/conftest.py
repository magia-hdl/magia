import sys
from contextlib import contextmanager
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory

import pytest

from magia import Elaborator, Module


@contextmanager
def elaborate_to_file(module: Module) -> str:
    with NamedTemporaryFile(mode="w", suffix=".sv") as f:
        f.write(Elaborator.to_string(module))
        f.flush()
        yield f.name


sys.modules["pytest"].elaborate_to_file = elaborate_to_file


@pytest.fixture()
def temp_build_dir():
    with TemporaryDirectory() as tmpdir:
        yield str(Path(tmpdir).absolute())
