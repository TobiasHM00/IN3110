"""Test script for hand-in version of the student's directory.
Does not check if "by_gas" and "figures" have the correct content (which is the solution of the assignment), only
if they exist and are non-empty.
"""
from pathlib import Path

import pytest

# Path to the students assignment2 directory
submission_dir = Path(__file__).parents[1].absolute()


@pytest.mark.parametrize(
    "expected",
    [
        (submission_dir / "analytic_tools"),
        (submission_dir / "pollution_data"),
        (submission_dir / "pollution_data_restructured"),
        (submission_dir / "tests"),
        (submission_dir / "analyze_pollution_data.py"),
        (submission_dir / "pyproject.toml"),
        (submission_dir / "README.md"),
    ],
)
def test_handin_toplevel(expected):
    """Check that all required top-level files are present in submission_dir

    Parameters:
        - expected (Path): path to the file that must be checked
    Returns:
    None
    """
    content_toplevel = list(submission_dir.iterdir())
    assert expected in content_toplevel, f"Missing required object: {expected}"


@pytest.mark.parametrize(
    "expected",
    [
        (submission_dir / "analytic_tools" / "utilities.py"),
        (submission_dir / "analytic_tools" / "plotting.py"),
        (submission_dir / "tests" / "conftest.py"),
        (submission_dir / "tests" / "test_utilities.py"),
        (submission_dir / "tests" / "test_handin.py"),
    ],
)
def test_modules_present(expected):
    """Check that all required modules are present in submission_dir

    Parameters:
        - expected (Path): path to the file that must be checked
    Returns:
    None
    """
    assert expected.exists(), f"File {expected} does not exist"


def test_handin_by_gas_dir():
    """Check that the required subdirectory "by_gas"
    is present in the pollution_data_restructure and non-empty
    """
    pollution_data_restructured = (
        Path(__file__).parents[1].absolute() / "pollution_data_restructured"
    )
    assert (pollution_data_restructured / "by_gas") in list(
        pollution_data_restructured.iterdir()
    ), "Missing pollution_data_restructured/by_gas dir"
    assert (
        list((pollution_data_restructured / "by_gas").iterdir()) != []
    ), "pollution_data_restructured/by_gas dir is empty"


def test_handin_figures_dir():
    """Check that the required subdirectory "figures"
    is present in the pollution_data_restructure and non-empty
    """
    pollution_data_restructured = (
        Path(__file__).parents[1].absolute() / "pollution_data_restructured"
    )
    assert (pollution_data_restructured / "figures") in list(
        pollution_data_restructured.iterdir()
    ), "Missing pollution_data_restructured/figures dir"
    assert (
        list((pollution_data_restructured / "figures").iterdir()) != []
    ), "pollution_data_restructured/figures dir is empty"
