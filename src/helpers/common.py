import os
import numpy as np
from PIL import Image
import cv2

def get_data_dir():
    return os.path.abspath(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            '..',
            '..',
            'data'
        )
    )

def process_image_from_array(image_array, processing_type):
    processed_image_array = image_array

    # TODO: implement processing type

    processed_image_array = cv2.cvtColor(processed_image_array, cv2.COLOR_BGR2GRAY)
    processed_image_array = cv2.Canny(processed_image_array, threshold1=200, threshold2=300)

    return processed_image_array

def process_image(image_path, processing_type):
    processed_image_array = process_image_from_array(
        np.array(Image.open(image_path)),
        processing_type
    )

    return Image.fromarray(processed_image_array)
