from __future__ import print_function

import argparse

from controller import Slot_Game_Controller

if __name__ == '__main__':

  parser = argparse.ArgumentParser(description="Play a slot machine.")

  parser.add_argument("-t", action="store_true")

  args = parser.parse_args()

  if args.t:
    # Do the test
    print("Running test sequence...\n")

    # Test the ui
    from slot_machines import Liberty_Bell_Machine

    slot_machine = Liberty_Bell_Machine()

    from user_interfaces.rpi_ui import Slot_RPI_UI
    ui = Slot_RPI_UI(slot_machine.reels)
    ui.test()

  else:

    controller = Slot_Game_Controller()
