"""Basic tests for the package

Tests that the package is installed and importable.

These tests should pass after task 1,
before you've done any implementation.
"""
from pathlib import Path

import numpy as np
import pytest

test_dir = Path(__file__).absolute().parent


def test_import():
    """Can we import our package at all"""
    import in3110_instapy  # noqa


@pytest.mark.parametrize(
    "filter_name",
    ["color2gray", "color2sepia"],
)
@pytest.mark.parametrize(
    "implementation",
    ["python", "numpy", "numba"],
)
def test_get_filter(filter_name, implementation):
    """Can we load our filter functions"""
    import in3110_instapy  # noqa

    filter_function = in3110_instapy.get_filter(filter_name, implementation)


def test_io():
    """Can we import and use our io utilities"""
    from in3110_instapy import io

    image = io.read_image(test_dir.joinpath("rain.jpg"))
    assert isinstance(image, np.ndarray)
    assert len(image.shape) == 3
    assert image.dtype == np.uint8
    assert image.shape[2] == 3
