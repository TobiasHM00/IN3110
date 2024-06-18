import random
import numpy as np
from in3110_instapy.python_filters import python_color2gray, python_color2sepia


def test_color2gray(image):
    # run color2gray
    gray_image = python_color2gray(image)
    
    # check that the result has the right shape, type
    assert gray_image.shape == image.shape
    assert gray_image.dtype == np.uint8

    for _ in range(3):
        row = random.randint(0, image.shape[0])
        col = random.randint(0, image.shape[1])
        r, g, b = image[row, col]
        grey_value = int(0.21 * r + 0.72 * g + 0.07 * b)
        assert np.all(gray_image[row, col][0] == grey_value)
        

def test_color2sepia(image):
    # run color2sepia
    sepia_image = python_color2sepia(image)
    # check that the result has the right shape, type
    assert sepia_image.shape == image.shape
    assert sepia_image.dtype == np.uint8
    
    # verify some individual pixel samples
    # according to the sepia matrix
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
