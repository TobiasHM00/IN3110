"""Cython implementation of filter functions"""
from __future__ import annotations

import cython as C
import numpy as np

if not C.compiled:
    raise ImportError(
        "Cython module not compiled! Check setup.py and make sure this package has been installed, not just imported in-place, e.g. `pip install --editable .`."
    )

from cython.cimports.libc.stdint import uint8_t  # noqa

# we may need a 'const uint8_t' type to make sure we accept 'read-only' arrays
const_uint8_t = C.typedef("const uint8_t")
float64_t = C.typedef(C.double)


def cython_color2gray(image):
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    ...


def cython_color2sepia(image):
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    ...
