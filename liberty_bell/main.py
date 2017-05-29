#!/usr/bin/python
from __future__ import absolute_import
import argparse
from liberty_bell.main_controller import Main_Controller

if __name__ == '__main__':

    # Determine which type of user interface to present
    parser = argparse.ArgumentParser(description="Liberty Bell")
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
