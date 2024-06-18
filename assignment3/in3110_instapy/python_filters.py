"""pure Python implementation of image filters"""
from __future__ import annotations

import numpy as np
from in3110_instapy import io

def python_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    gray_image = np.empty_like(image)
    
    for row in range(image.shape[0]):
        for col in range(image.shape[1]):
            r, g, b = image[row, col]
            gray_pixel = (0.21 * r + 0.72 * g + 0.07 * b)
            gray_image[row, col] = gray_pixel
    
    gray_image = gray_image.astype("uint8")
    return gray_image


def python_color2sepia(image: np.array) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: sepia_image
    """
    sepia_image = np.empty_like(image)
    # Iterate through the pixels
    # applying the sepia matrix
    sepia_matrix = [
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168],
        [0.272, 0.534, 0.131],
    ]

    for row in range(image.shape[0]):
        for col in range(image.shape[1]):
            r, g, b = image[row, col]
            
            sepia_red = min(255, (r*sepia_matrix[0][0] + g*sepia_matrix[0][1] + b*sepia_matrix[0][2]))
            sepia_green = min(255, (r*sepia_matrix[1][0] + g*sepia_matrix[1][1] + b*sepia_matrix[1][2]))
            sepia_blue = min(255, (r*sepia_matrix[2][0] + g*sepia_matrix[2][1] + b*sepia_matrix[2][2]))
            sepia_image[row, col] = (sepia_red, sepia_green, sepia_blue)

    # Return image
    # don't forget to make sure it's the right type!
    sepia_image = sepia_image.astype("uint8")
    return sepia_image
