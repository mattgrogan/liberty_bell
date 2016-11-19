#!/usr/bin/python

import argparse
import sys

from main_controller import Main_Controller

if __name__ == '__main__':

  parser = argparse.ArgumentParser(description="Liberty Bell")
  parser.add_argument("-output", required=False, choices=[
                      "gui", "rpi"], default="rpi")
  parser.add_argument("-t", action="store_true")

  args = parser.parse_args()

  controller = Main_Controller()

  # Running on the Raspberry Pi
  if args.output == "rpi":
    from ui.rpi import Rpi_UI
    ui = Rpi_UI(controller)
  elif args.output == "gui":
    from ui.gui import Gui
    ui = Gui(controller)

  ui.mainloop()
