import sys
import os
import json
import glob
import time
import datetime
from helpers.common import *
from helpers.image import *

# Preparation
now = datetime.datetime.now()
data_dir = get_data_dir()
args = get_args()

activity = args['activity']
mode = args['mode']
processed_images = []
activity_raw_dir = os.path.join(data_dir, activity, 'raw')
processed_dir = os.path.join(data_dir, activity, 'processed', mode)
processed_images_file_path = os.path.join(
    processed_dir, 'processed_images.txt')  # Saves all the processed images
# Saves the final processed data, such as: left, right, forward, backward, ... means, ONLY the core data (as opposed to all the raw data we get while capturing)
processed_data_file_path = os.path.join(processed_dir, 'data.txt')

# Functions


def get_processed_images():
    processed_images_file = open(processed_images_file_path, 'r+').read()
    processed_images = processed_images_file.split("\n")
    processed_data = list(filter(None, processed_images))

    return processed_images


def get_activity_raw_session_dirs():
    activity_raw_session_dirs = [
        x[0] for x in os.walk(activity_raw_dir)
    ]

    if len(activity_raw_session_dirs) is 0:
        sys.exit('Exiting. Did not found any sessions for this activity')

    # Remove first object, as it's the directory itself
    activity_raw_session_dirs.pop(0)

    return activity_raw_session_dirs


def get_session_directory_images(session_directory_log_file_path):
    session_directory_log_file = open(
        session_directory_log_file_path, 'r+').read()
    session_directory_images = session_directory_log_file.split("\n")
    session_directory_images = list(filter(None, session_directory_images))

    return session_directory_images


def do_image_processing(image_data):
    image_path = image_data['image']['path']

    print('Processing image {0} ...'.format(image_path))
    sys.stdout.flush()

    image_name = os.path.basename(image_path)
    processed_image_path = os.path.join(processed_dir, image_name)

    processed_image = process_image(image_path)
    processed_image.save(processed_image_path)

    with open(processed_images_file_path, 'a') as file_stream:
        file_stream.write(image_path + "\n")

    with open(processed_data_file_path, 'a') as file_stream:
        file_stream.write(json.dumps(
            get_image_processing_data_row(
                processed_image_path,
                image_data['inputs']
            )
        ) + "\n")


def do_session_directory_processing(session_directory, session_directory_images):
    global processed_images

    print('Processing images from directory {0} ...'.format(session_directory))
    sys.stdout.flush()

    for image_raw_data in session_directory_images:
        image_data = json.loads(image_raw_data)
        image_path = image_data['image']['path']

        if image_path not in processed_images:
            do_image_processing(image_data)

    print('Images from directory {0} were all successfully processed.'.format(session_directory))
    print('-' * 32)
    sys.stdout.flush()


# Main
def process():
    global processed_images

    # Prepare folders and files
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)

    if not os.path.exists(processed_images_file_path):
        processed_images_file = open(processed_images_file_path, 'w+').read()

    if not os.path.exists(processed_data_file_path):
        processed_images_file = open(processed_data_file_path, 'w+').read()

    # General information
    print('Start at {0}'.format(now))
    print('=' * 32)
    print('Activity: {0}'.format(activity))
    print('=' * 32)
    print('Mode: {0}'.format(mode))
    print('=' * 32)
    sys.stdout.flush()

    # Already processed images
    processed_images = get_processed_images()
    print('Already processed images: {0}'.format(len(processed_images)))
    print('=' * 32)
    sys.stdout.flush()

    # Activity session directories
    activity_raw_session_dirs = get_activity_raw_session_dirs()
    print('Found activity session directories:')
    print(activity_raw_session_dirs)
    print('=' * 32)
    sys.stdout.flush()

    # Start processing per directory
    print('Starting to process session directories ...')
    print('=' * 32)
    print('=' * 32)
    print('=' * 32)
    sys.stdout.flush()

    for session_directory in activity_raw_session_dirs:
        session_directory_log_file_path = os.path.join(
            session_directory, 'log.txt')

        # Jump out, as we did not find any data in this session
        if not os.path.exists(session_directory_log_file_path):
            print('Skip directory. Did not found any log file in {0}'.format(
                session_directory))
            print('=' * 32)
            sys.stdout.flush()

            continue

        session_directory_images = get_session_directory_images(
            session_directory_log_file_path)

        print('Processing directory {0}'.format(session_directory))
        print('Found {0} images'.format(len(session_directory_images)))
        sys.stdout.flush()

        if len(session_directory_images) > 0:
            do_session_directory_processing(
                session_directory, session_directory_images)

        print('Directory {0} was successfully processed.'.format(session_directory))
        print('=' * 32)
        sys.stdout.flush()

    print('Session directories were all successfully processed.')
