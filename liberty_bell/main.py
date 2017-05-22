#!/usr/bin/python
from __future__ import absolute_import

import argparse

from liberty_bell.main_controller import Main_Controller
from liberty_bell.slot_machine_controller import Slot_Machine_Controller
from liberty_bell.slot_machines.gold_award_machine import Gold_Award_Machine
from liberty_bell.slot_machines.liberty_bell_machine import \
    Liberty_Bell_Machine

from liberty_bell.ui.liberty_bell_ui import Liberty_Bell_UI

if __name__ == '__main__':

  parser = argparse.ArgumentParser(description="Liberty Bell")
  parser.add_argument("-output", required=False, choices=[
                      "gui", "rpi"], default="rpi")
  parser.add_argument("-t", action="store_true")

  args = parser.parse_args()

  controller = Main_Controller()

  if args.output == "rpi":
    from liberty_bell.ui.rpi import Rpi_UI
    ui = Rpi_UI()
  elif args.output == "gui":
    from liberty_bell.ui.gui import Gui
    ui = Gui()

  main_ui = Liberty_Bell_UI(ui)

  liberty_bell = Slot_Machine_Controller(Liberty_Bell_Machine(), main_ui)
  gold_award = Slot_Machine_Controller(Gold_Award_Machine(), main_ui)

  controller.add_games([liberty_bell, gold_award])
  controller.ui = main_ui
  controller.ui.attach(controller.handle_input)
  ui.run_callback = controller.run
  ui.ready()

  try:
    ui.mainloop()
  finally:
    ui.shutdown()
