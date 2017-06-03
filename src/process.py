import sys, os, glob, time, datetime
from PIL import Image
import cv2
from helpers.common import *

# Preparation
now = datetime.datetime.now()
data_dir = get_data_dir()
activity = len(sys.argv) > 1 and sys.argv[1] or 'general'
processing_type = len(sys.argv) > 2 and sys.argv[2] or 'black_and_white' # what type of processing will we do on this images?
activity_raw_dir = os.path.join(data_dir, activity, 'raw')
processed_dir = os.path.join(data_dir, activity, 'processed', processing_type)
if not os.path.exists(processed_dir):
    os.makedirs(processed_dir)

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
    
    # Already processed images
    processed_images_file_path = os.path.join(processed_dir, 'files.txt')
    if os.path.exists(processed_images_file_path):
        processed_images_file = open(processed_images_file_path, 'r+').read()
    else:
        processed_images_file = open(processed_images_file_path, 'w+').read()
        
    processed_images = processed_images_file.split("\n")
    processed_images = [x for x in processed_images if x != ''] # TODO: find a quicker solution? filter()?
    
    print('Already processed images: {0}'.format(len(processed_images)))
    print('=' * 32)
    
    # Activity session directories
    activity_raw_session_dirs = [
        x[0] for x in os.walk(activity_raw_dir)
    ]
    activity_raw_session_dirs.pop(0) # Remove first object, as it's the directory itself
    
    print('Found activity session directories:')
    print(activity_raw_session_dirs)
    print('=' * 32)
    
    print('Starting processing sessions directories ...')
    print('=' * 32)
    for directory in activity_raw_session_dirs:
        directory_images = glob.glob(
            os.path.join(
                directory,
                '*.png'
            )
        )
        print('Processing directory {0}'.format(directory))
        print('Found {0} images'.format(len(directory_images)))
        
        if len(directory_images) > 0:
            print('Processing images from directory {0}'.format(directory))
            
            for image_path in directory_images:
                if image_path not in processed_images:
                    print('Processing image {0}'.format(image_path))
                    image_name = os.path.basename(image_path)
                    processed_image = process_image(image_path, processing_type)
                    processed_image.save(
                        os.path.join(processed_dir, image_name)
                    )
                    
                    with open(processed_images_file_path, 'a') as log_file:
                        log_file.write(image_path + "\n")
                else:
                    print('The image {0} was already processed'.format(image_path))
                
            print('Images from directory {0} processed'.format(directory))
            print('-' * 32)
        
        print('Directory {0} processed'.format(directory))
        print('=' * 32)
    
    # TODO
