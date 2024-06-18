from pathlib import Path

import pytest

assignment_dir = Path(__file__).absolute().parents[1]


@pytest.mark.parametrize(
    "filename",
    [
        "pyproject.toml",
        "README.md",
        "app.py",
        "strompris.py",
        "templates/strompris.html",
        "docs",
    ],
)
def test_files(filename):
    assert Path(filename).exists()


@pytest.mark.parametrize(
    "filename",
    [
        "klima/app.py",
        "templates/activity.html",
    ],
)
def test_optional_files(filename):
    if not Path(filename).exists():
        pytest.skip(f"{filename} for optional task does not exist")
