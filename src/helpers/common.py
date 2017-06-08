import os
import cv2
import argparse
import numpy as np
from PIL import Image, ImageGrab


def prepare_args():
    parser = argparse.ArgumentParser(description='Deep Gamer')

    parser.add_argument(
        'action',
        help='Which action should be triggered (available: capture, evaluate, process & train)?',
        choices=['capture', 'process', 'train', 'evaluate']
    )
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
    parser.add_argument(
        '-n',
        '--force-new-model',
        help='Should we force a new model to be trained?',
        action='store_true'
    )

    return parser.parse_args()


def get_args():
    args = prepare_args()

    return {
        'action': args.action,
        'activity': args.activity,
        'mode': args.mode,
        'force_new_model': args.force_new_model,
    }


def grab_image(file_path=False, file_format='PNG', **options):
    image = ImageGrab.grab()

    if file_path != False:
        image.save(file_path, file_format, **options)

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
        mode = None  # https://stackoverflow.com/questions/32192671/pil-image-mode-i-is-grayscale

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

def get_from_and_to_index(iteration, batch_size, total_size):
    from_index = iteration * batch_size
    to_index = from_index + batch_size
    modulo = to_index % total_size

    # TODO: figure out the real formula
    if to_index > total_size:
        to_index = modulo
        from_index = to_index - batch_size
        
        if from_index < 0:
            from_index = 0
            to_index = batch_size

    return from_index, to_index


def save_model(model):
    # TODO: make backups/archives?
    model.save(network_model_path)


def get_prediction(model, X, controls_map):
    action = None

    prediction = model.predict([X])
    prediction = prediction[0]

    max_index = np.argmax(prediction)

    # View controls_map dict to see, which output corresponds to which action
    for control, output in controls_map.items():
        control_max_index = np.argmax(output)
        if max_index == control_max_index:
            action = control

    return {
        'action': action,
        'action_confidence': prediction[max_index],
        'raw': prediction,
    }
