"""numpy implementation of image filters"""
from __future__ import annotations

import numpy as np

def numpy_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """

    gray_image = np.empty_like(image)

    # Hint: use numpy slicing in order to have fast vectorized code
    gray_image[:, :, 0] = 0.21*image[:, :, 0] + 0.72*image[:, :, 1] + 0.07*image[:, :, 2]
    gray_image[:, :, 1] = 0.21*image[:, :, 0] + 0.72*image[:, :, 1] + 0.07*image[:, :, 2]
    gray_image[:, :, 2] = 0.21*image[:, :, 0] + 0.72*image[:, :, 1] + 0.07*image[:, :, 2]
        
    # Return image (make sure it's the right type!)
    gray_image = gray_image.astype("uint8")
    return gray_image


def numpy_color2sepia(image: np.array, k: float = 1) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
        k (float): amount of sepia (optional)

    The amount of sepia is given as a fraction, k=0 yields no sepia while
    k=1 yields full sepia.

    (note: implementing 'k' is a bonus task,
        you may ignore it)

    Returns:
        np.array: sepia_image
    """

    if not 0 <= k <= 1:
        # validate k (optional)
        raise ValueError(f"k must be between [0-1], got {k=}")

    sepia_image = np.empty_like(image)
    
    # define sepia matrix (optional: with stepless sepia changes)
    sepia_matrix = np.array(
        [
            [1.0 - 0.607 * k, 0.0 + 0.769 * k, 0.0 + 0.189 * k],
            [0.0 + 0.349 * k, 1.0 - 0.314 * k, 0.0 + 0.168 * k],
            [0.0 + 0.272 * k, 0.0 + 0.534 * k, 1.0 - 0.869 * k]
        ]
    )

    # HINT: For version without adaptive sepia filter, use the same matrix as in the pure python implementation
    # any way works, but you could use an Einstein sum to apply pixel transform matrix
    # or a tensor dot product, for example
    sepia_image = np.dot(image, sepia_matrix.T)

    # Check which entries have a value greater than 255 and set it to 255 since we can not display values bigger than 255
    sepia_image = np.clip(sepia_image, 0, 255)

    # Return image (make sure it's the right type!)
    sepia_image = sepia_image.astype("uint8")
    return sepia_image
