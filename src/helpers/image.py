import numpy as np
from PIL import Image
from helpers.custom import *

def process_image(image, return_array=False):
    if type(image) is str:
        image = Image.open(image)

    processed_image_array = preprocess_image(image)

    if return_array:
        return processed_image_array

    return Image.fromarray(processed_image_array)
