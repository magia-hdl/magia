from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from magia_flow.simulation.verilator import init_verilator

init_verilator()


@pytest.fixture()
def temp_build_dir():
    with TemporaryDirectory() as tmpdir:
        yield str(Path(tmpdir).absolute())
