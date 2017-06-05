import os
import cv2
import argparse
import numpy as np
from PIL import Image, ImageGrab

def prepare_args():
    parser = argparse.ArgumentParser(description='Deep Gamer')

    parser.add_argument(
        '-a',
        '--activity',
        help='Which activity will you be doing (ex.: driving, walking, running, ...)?',
        default='general'
    )
    parser.add_argument(
        '-m',
        '--mode',
        help='Which mode should we use when processing/evaluating the raw data? Usefull when processing/evaluating/testing multiple results with the same raw data.',
        default='default'
    )

    return parser.parse_args()

def get_args():
    args = prepare_args()

    return {
        'activity': args.activity,
        'mode': args.mode,
    }

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
