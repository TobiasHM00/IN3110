"""Command-line (script) interface to instapy"""
from __future__ import annotations

import argparse
import sys

from in3110_instapy.timing import time_one as to
import in3110_instapy
import numpy as np
from PIL import Image

from . import get_filter, io


def run_filter(
    file: str,
    out_file: str = None,
    implementation: str = "python",
    filter: str = "color2gray",
    scale: int = 1,
    runtime: bool = None,
) -> None:
    """Run the selected filter"""
    # load the image from a file
    image = io.read_image(file)
    
    if scale != 1:
        # Resize image, if needed
        openFile = Image.open(file)
        resized = openFile.resize((int(openFile.width*scale), int(openFile.height*scale)))
        image = np.asarray(resized)

    # Apply the filter
    filter_name = get_filter(filter, implementation)
    filtered = filter_name(image)
    if out_file:
        # save the file
        io.write_image(filtered, out_file)
    else:
        # not asked to save, display it instead
        io.display(filtered)
    
    if runtime:
        runTimed = to(filter_name, image)
        print(f"Average time over 3 runs: {implementation}_{filter}: {runTimed:.3}s")


def main(argv=None):
    """Parse the command-line and call run_filter with the arguments"""
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser()

    # filename is positional and required
    parser.add_argument("file", help="The filename to apply filter to")
    parser.add_argument("-o", "--out", help="The output filename")

    # Add required arguments
    parser.add_argument("-g", "--gray", action="store_true", help="Select gray filter")
    parser.add_argument("-se", "--sepia", action="store_true", help="Select sepia filter")
    parser.add_argument("-sc", "--scale", type=float, default=1.0, help="Scale factor to resize image")
    parser.add_argument("-i", "--implementation", choices=["python", "numba", "numpy"], default="python", help="The implementation")
    parser.add_argument("-r", "--runtime", action="store_true", help="Tracks runtime to the different filters")

    # parse arguments and call run_filter
    args = parser.parse_args(argv)
    if args.sepia:
        filter = "color2sepia"
    else:
        filter = "color2gray"
        
    if args.runtime:
        runtime = True
    else:
        runtime = False
    
    run_filter(args.file, args.out, args.implementation, filter, args.scale, runtime)
