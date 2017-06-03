import sys, os, time
import cv2
import numpy as np
from helpers.common import *

# Main
if __name__ == "__main__":
    last_time = time.time()

    while True:
        image = grab_image()

        processed_image = np.array(process_image(image))

        # Vision
        cv2.namedWindow('AIVision', cv2.WINDOW_NORMAL)
        cv2.imshow('AIVision', processed_image)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

        last_time = time.time()
