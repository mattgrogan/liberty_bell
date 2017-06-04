#!/usr/bin/python
from __future__ import absolute_import

from argparse import ArgumentParser
from liberty_bell.main_controller import Main_Controller

if __name__ == '__main__':

    # Arguments determine which type of ui to present
    parser = ArgumentParser(description="Liberty Bell")
    parser.add_argument("-output",
                        required=False,
                        choices=["gui", "rpi"],
                        default="rpi")
    parser.add_argument("-t", action="store_true")
    args = parser.parse_args()

    # Instantiate the controller
    controller = Main_Controller(ui_type=args.output)

    try:
        controller.start()
    finally:
        controller.shutdown()
