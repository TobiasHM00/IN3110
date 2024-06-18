"""instapy: image filters in Python"""
from __future__ import annotations

import importlib

# changes the parameters to be able to use them for every function i want to
def get_filter(filter: str, implementation: str):
    """Return the filter function by name

    Assumes filters are named e.g.in3110_instapy.python_filters.python_color2gray.

    Args:

        filter (str):
            The name of the filter ('color2gray' or 'color2sepia')
        implementation (str):
            The name of the implementation (python, cython, etc.)

    Returns:
        filter_function (function):
            The filter function, which should take an image
            (a 3D numpy array of uint8)
            and return the filtered image
            (numpy array of same shape and type as input)
    """

    # get the module (instapy.python_filters)
    module = importlib.import_module(f"in3110_instapy.{implementation}_filters")
    # construct filter function name (python_color2gray)
    filter_name = f"{implementation}_{filter}"
    # return the resolved function (instapy.python.python_color2gray)
    return getattr(module, filter_name)
