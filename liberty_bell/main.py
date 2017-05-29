#!/usr/bin/python
from __future__ import absolute_import

import argparse

from liberty_bell.main_controller import Main_Controller
from liberty_bell.slot_machine_controller import Slot_Machine_Controller
from liberty_bell.slot_machines.gold_award_machine import Gold_Award_Machine
from liberty_bell.slot_machines.liberty_bell_machine import \
    Liberty_Bell_Machine


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Liberty Bell")

    parser.add_argument("-output",
                        required=False,
                        choices=["gui", "rpi"],
                        default="rpi")

    parser.add_argument("-t", action="store_true")

    args = parser.parse_args()

    controller = Main_Controller(ui_type=args.output)

    controller.ui.attach(controller.handle_input)

    try:
        controller.mainloop()
    finally:
        controller.shutdown()
