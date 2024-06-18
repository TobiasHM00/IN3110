import random
import numpy as np
import numpy.testing as nt
from in3110_instapy.numpy_filters import numpy_color2gray, numpy_color2sepia


def test_color2gray(image, reference_gray):
    gray_image = numpy_color2gray(image)
    
    assert gray_image.shape == image.shape
    assert gray_image.dtype == np.uint8
    
    nt.assert_allclose(gray_image, reference_gray)
    
    for _ in range(3):
        row = random.randint(0, image.shape[0])
        col = random.randint(0, image.shape[1])
        r, g, b = image[row, col]
        expected_gray_pixel = int(0.21 * r + 0.72 * g + 0.07 * b)
        assert np.all(gray_image[row, col] == expected_gray_pixel)
        

def test_color2sepia(image, reference_sepia):
    sepia_image = numpy_color2sepia(image)
    
    assert sepia_image.shape == image.shape
    assert sepia_image.dtype == np.uint8
    
    nt.assert_allclose(sepia_image, reference_sepia, atol=1)
    
    sepia_matrix = [
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168],
        [0.272, 0.534, 0.131],
    ]
    
    for _ in range(3):
        row = random.randint(0, image.shape[0])
        col = random.randint(0, image.shape[1])

        r, g, b = image[row, col]
        sepia_red = min(255, int(r*sepia_matrix[0][0] + g*sepia_matrix[0][1] + b*sepia_matrix[0][2]))
        sepia_green = min(255, int(r*sepia_matrix[1][0] + g*sepia_matrix[1][1] + b*sepia_matrix[1][2]))
        sepia_blue = min(255, int(r*sepia_matrix[2][0] + g*sepia_matrix[2][1] + b*sepia_matrix[2][2]))
        expected_sepia_value = (sepia_red, sepia_green, sepia_blue)
        assert np.all(sepia_image[row, col] == expected_sepia_value)
        