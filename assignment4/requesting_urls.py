"""
Task 1.1 - requesting HTML documents with HTTP
"""
from __future__ import annotations

import requests


def get_html(url: str, params: dict | None = None, output: str | None = None):
    """Get an HTML page and return its contents.

    Args:
        url (str):
            The URL to retrieve.
        params (dict, optional):
            URL parameters to add.
        output (str, optional):
            (optional) path where output should be saved.
    Returns:
        html (str):
            The HTML of the page, as text.
    """
    # passing the optional parameters argument to the get function
    response = requests.get(url, params)
    
    # want to check if the request was successful
    if response.status_code != 200:
        raise Exception(f"Failed to retreive the page. Status code: {response.status_code}")

    html_str = response.text

    if output:
        # if output is specified, the request url and text content are written
        # to the file at `output`.
        # The first line should be the URL,
        # and the rest of the file should be the response contents.
        with open(output, "w") as f:
            f.write(url)
            f.write(html_str)

    return html_str
