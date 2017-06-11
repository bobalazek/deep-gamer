import sys
import os
import time
import datetime
import json
from helpers.common import *


class CaptureAction:

    network = None
    is_capturing = False  # If we should be capturing
    inputs = None  # Saves the current input on every tick

    def __init__(self, network):
        args = get_args()
        now = datetime.datetime.now()

        self.network = network

        session_id = now.strftime('%Y-%m-%d_%H%M%S')
        self.session_dir = os.path.join(
            get_data_dir(), args['activity'], 'raw', session_id)

    def capture_image(self, timestamp):
        filename = timestamp.replace(':', '') + '.jpg'
        filepath = os.path.join(self.session_dir, filename)

        # TODO: batch image save?
        grab_image(file_path=filepath, file_format='JPEG')

        return filename, filepath

    def do_capture(self):
        now = datetime.datetime.now()
        timestamp = now.isoformat()

        if check_for_capturing_hotkeys(
                self.inputs['keyboard'], self.network.toggle_capture_hotkeys):
            self.is_capturing = not self.is_capturing

        if self.is_capturing:
            image_name, image_path = self.capture_image(timestamp)
            data = {
                'timestamp': timestamp,
                'image': {
                    'name': image_name,
                    'path': image_path,
                },
                'inputs': self.inputs,
            }

            with open(os.path.join(self.session_dir, 'log.txt'), 'a') as log_file:
                log_file.write(json.dumps(data) + "\n")

        return self.is_capturing

    def capture(self):
        now = datetime.datetime.now()
        last_time = time.time()

        # Prepare folders and files
        if not os.path.exists(self.session_dir):
            os.makedirs(self.session_dir)

        print('Start at {0}'.format(now))
        print('=' * 32)
        print('To start/stop capturing, press: {0}'.format(
            ' & '.join(self.network.toggle_capture_hotkeys)))
        print('=' * 32)
        sys.stdout.flush()

        while True:
            self.inputs = get_inputs()

            if self.do_capture():
                print('Last execution took {0} seconds.'.format(
                    time.time() - last_time))
                print(
                    'Controls: {0}'.format(
                        self.network.get_controls_from_inputs(
                            self.inputs)))
                sys.stdout.flush()

            last_time = time.time()
