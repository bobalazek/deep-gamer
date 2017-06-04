import sys, os, time
from helpers.common import *

# Main
if __name__ == "__main__":
    last_time = time.time()

    while True:
        original_image = grab_image()
        processed_image = process_image(original_image)

        print('Last execution took {0} seconds.'.format(time.time() - last_time))

        if not show_preview_window(processed_image):
            break

        last_time = time.time()
