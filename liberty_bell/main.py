#!/usr/bin/python
from __future__ import absolute_import

from argparse import ArgumentParser
from liberty_bell.main_controller import MainController

if __name__ == '__main__':

    # Arguments determine which type of ui to present
    parser = ArgumentParser(description="Liberty Bell")
    parser.add_argument("-output",
                        required=False,
                        choices=["gui", "rpi"],
                        default="rpi")

    args = parser.parse_args()

    # Instantiate the controller
    controller = MainController(ui_type=args.output)

    #try:
    controller.start()
    #finally:
    #    controller.shutdown()
