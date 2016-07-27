from __future__ import print_function

import argparse

from controller import Slot_Game_Controller

if __name__ == '__main__':

  parser = argparse.ArgumentParser(description="Play a slot machine.")

  parser.add_argument("-ui", choices=["text", "gui", "rpi"])
  parser.add_argument("-t", action="store_true")

  args = parser.parse_args()

  if args.t:
    # Do the test
    print("Running test sequence...\n")

    # Test the winner paid display
    from user_interfaces.numeric_display import SevenSegment_Numeric_Display
    winner_paid_led = SevenSegment_Numeric_Display(
        name="Winner paid", address=0x70)
    winner_paid_led.test()

  else:

    if args.ui == "text":
      ui = "TEXT_UI"
    elif args.ui == "gui":
      ui = "GUI_UI"
    elif args.ui == "rpi":
      ui = "RPI_UI"
    else:
      raise ValueError("Invalid user interface specified.")

    controller = Slot_Game_Controller(ui)
