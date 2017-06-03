import sys, os, json, glob, time, datetime
from helpers.common import *

# Preparation
now = datetime.datetime.now()
data_dir = get_data_dir()
activity = len(sys.argv) > 1 and sys.argv[1] or 'general'
processing_type = len(sys.argv) > 2 and sys.argv[2] or 'default' # what type of processing will we do on this images?
activity_raw_dir = os.path.join(data_dir, activity, 'raw')
processed_dir = os.path.join(data_dir, activity, 'processed', processing_type)
if not os.path.exists(processed_dir):
    os.makedirs(processed_dir)

processed_images_file_path = os.path.join(processed_dir, 'processed_images.txt') # Saves all the processed images
processed_data_file_path = os.path.join(processed_dir, 'data.txt') # Saves the final processed data, such as: left, right, forward, backward, ... means, ONLY the core data (as opposed to all the raw data we get while capturing)
    
# Functions
def prepare_files():
    if not os.path.exists(processed_images_file_path):
        processed_images_file = open(processed_images_file_path, 'w+').read()

    if not os.path.exists(processed_data_file_path):
        processed_images_file = open(processed_data_file_path, 'w+').read()

def get_processed_images():
    processed_images_file = open(processed_images_file_path, 'r+').read()

    processed_images = processed_images_file.split("\n")
    processed_images = [x for x in processed_images if x != ''] # TODO: find a quicker solution? filter()?
    
    return processed_images

def get_activity_raw_session_dirs():
    activity_raw_session_dirs = [
        x[0] for x in os.walk(activity_raw_dir)
    ]

    if len(activity_raw_session_dirs) == 0:
        sys.exit('Exiting. Did not found any sessions for this activity')

    activity_raw_session_dirs.pop(0) # Remove first object, as it's the directory itself

    return activity_raw_session_dirs

def get_session_directory_images(session_directory_log_file_path):
    session_directory_log_file = open(session_directory_log_file_path, 'r+').read()
    session_directory_images = session_directory_log_file.split("\n")
    session_directory_images = [x for x in session_directory_images if x != ''] # TODO: find a quicker solution? filter()?

    return session_directory_images

def do_image_processing(image_data):
    image_path = image_data['image']['path']

    print('Processing image {0}'.format(image_path))
    image_name = os.path.basename(image_path)
    processed_image_path = os.path.join(processed_dir, image_name)

    processed_image = process_image(image_path, processing_type)
    processed_image.save(processed_image_path)

    with open(processed_images_file_path, 'a') as file_stream:
        file_stream.write(image_path + "\n")

    with open(processed_data_file_path, 'a') as file_stream:
        file_stream.write(json.dumps({
            'image_path': processed_image_path,
            'controls': {
                'forward': image_data['inputs']['keyboard']['w'] or 
                    image_data['inputs']['gamepad']['axes']['right_trigger'] > 0,
                'backward': image_data['inputs']['keyboard']['s'] or 
                    image_data['inputs']['gamepad']['axes']['left_trigger'] > 0,
                'left': image_data['inputs']['keyboard']['a'] or 
                    image_data['inputs']['gamepad']['axes']['left']['x'] < 0,
                'right': image_data['inputs']['keyboard']['d'] or 
                    image_data['inputs']['gamepad']['axes']['left']['x'] > 0,
            },
        }) + "\n")

def do_session_directory_processing(session_directory, session_directory_images):
    print('Processing images from directory {0}'.format(session_directory))

    for image_raw_data in session_directory_images:
        image_data = json.loads(image_raw_data)
        image_path = image_data['image']['path']

        if image_path not in processed_images:
            do_image_processing(image_data)
        else:
            print('The image {0} was already processed'.format(image_path))

    print('Images from directory {0} were processed'.format(session_directory))
    print('-' * 32)
    
# Main
if __name__ == "__main__":
    last_time = time.time()

    # General information
    print('Start at {0}'.format(now))
    print('=' * 32)
    print('Activity: {0}'.format(activity))
    print('=' * 32)
    print('Processing type: {0}'.format(processing_type))
    print('=' * 32)

    # Prepare files
    prepare_files()

    # Already processed images
    processed_images = get_processed_images()
    print('Already processed images: {0}'.format(len(processed_images)))
    print('=' * 32)

    # Activity session directories
    activity_raw_session_dirs = get_activity_raw_session_dirs()
    print('Found activity session directories:')
    print(activity_raw_session_dirs)
    print('=' * 32)

    # Start processing per directory
    print('Starting processing sessions directories ...')
    print('=' * 32)
    for session_directory in activity_raw_session_dirs:
        session_directory_log_file_path = os.path.join(session_directory, 'log.txt')

        # Jump out, as we did not find any data in this session
        if not os.path.exists(session_directory_log_file_path):
            print('Did not found any log file in {0}'.format(session_directory))
            continue

        session_directory_images = get_session_directory_images(session_directory_log_file_path)

        print('Processing directory {0}'.format(session_directory))
        print('Found {0} images'.format(len(session_directory_images)))

        if len(session_directory_images) > 0:
            do_session_directory_processing(session_directory, session_directory_images)

        print('Directory {0} processed'.format(session_directory))
        print('=' * 32)
