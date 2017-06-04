import sys, os, time
import cv2
from helpers.common import *

# Main
if __name__ == "__main__":
    last_time = time.time()

    while True:
        image = grab_image()

        processed_image = process_image(image, return_array=True)

        # Vision
        cv2.namedWindow('Vision', cv2.WINDOW_NORMAL)
        cv2.imshow('Vision', processed_image)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

        last_time = time.time()
