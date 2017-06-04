import os
import cv2
import numpy as np
from PIL import Image, ImageGrab

def grab_image(save_path=False):
    # TODO: fix -- not working in the MINGW64 terminal
    image = ImageGrab.grab()
    if save_path != False:
        image.save(save_path)

    return image

def get_data_dir():
    return os.path.abspath(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            '..',
            '..',
            'data'
        )
    )

def process_image_from_array(image_array, mode='default'):
    processed_image_array = image_array

    # TODO: implement mode

    processed_image_array = cv2.cvtColor(processed_image_array, cv2.COLOR_BGR2GRAY)
    processed_image_array = cv2.Canny(processed_image_array, threshold1=50, threshold2=250)

    return processed_image_array

def process_image(image, mode='default', return_array=False):
    if type(image) is str:
        image = Image.open(image)

    processed_image_array = process_image_from_array(
        np.array(image),
        mode
    )

    if return_array:
        return processed_image_array

    return Image.fromarray(processed_image_array)

def show_preview_window(images_array):
    final_images_array = []

    for image in images_array:
        mode = None # https://stackoverflow.com/questions/32192671/pil-image-mode-i-is-grayscale

        # TODO: also add other modes
        if image.mode is 'L':
            mode = cv2.COLOR_GRAY2RGB

        if mode is None:
            final_images_array.append(np.array(image))
        else:
            final_images_array.append(
                cv2.cvtColor(
                    np.array(image),
                    mode
                )
            )

    preview_image_array = np.hstack(final_images_array)

    # TODO: figure out why some colors are inversed

    cv2.namedWindow('Preview', cv2.WINDOW_NORMAL)
    cv2.imshow('Preview', preview_image_array)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()

        return False

    return True
