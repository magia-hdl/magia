from pathlib import Path
from tempfile import TemporaryDirectory

import pytest


@pytest.fixture()
def temp_build_dir():
    with TemporaryDirectory() as tmpdir:
        yield str(Path(tmpdir).absolute())
