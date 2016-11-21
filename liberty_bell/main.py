#!/usr/bin/python

import argparse
import sys

from main_controller import Main_Controller
from menu_controller import Menu_Controller
from slot_machine_menu_item import Slot_Machine_Menu_Item
from slot_machines.gold_award_machine import Gold_Award_Machine
from slot_machines.liberty_bell_machine import Liberty_Bell_Machine

if __name__ == '__main__':

  parser = argparse.ArgumentParser(description="Liberty Bell")
  parser.add_argument("-output", required=False, choices=[
                      "gui", "rpi"], default="rpi")
  parser.add_argument("-t", action="store_true")

  args = parser.parse_args()

  controller = Main_Controller()

  if args.output == "rpi":
    from ui.rpi import Rpi_UI
    ui = Rpi_UI(controller)
  elif args.output == "gui":
    from ui.gui import Gui
    ui = Gui(controller)

  controller.menu_controller = Menu_Controller(ui)

  liberty_bell = Slot_Machine_Menu_Item(Liberty_Bell_Machine(), ui)
  gold_award = Slot_Machine_Menu_Item(Gold_Award_Machine(), ui)

  controller.add_menu_item(liberty_bell)
  controller.add_menu_item(gold_award)

  try:
    ui.mainloop()
  finally:
    ui.shutdown()
