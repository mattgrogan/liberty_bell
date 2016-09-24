import sys
import time

from menu_controller import Menu_Controller
from slot_game_controller import Slot_Game_Controller
from slot_machines import Liberty_Bell_Machine
from ui import Slot_UI
from view_item_controller import View_Item_Controller


class Application_Controller(object):
  """ Control the application """

  def __init__(self):
    """ Initialize by linking up the UI """

    # Wire up the buttons
    self.ui = Slot_UI()
    self.ui.register("spin_pressed", self, self.spin_pressed_handler)
    self.ui.register("up_pressed", self, self.up_pressed_handler)
    self.ui.register("down_pressed", self, self.down_pressed_handler)
    self.ui.register("menu_pressed", self, self.menu_pressed_handler)
    self.ui.register("b1_pressed", self, self.b1_pressed_handler)
    self.ui.register("b2_pressed", self, self.b2_pressed_handler)
    self.ui.register("b3_pressed", self, self.b3_pressed_handler)

    self.liberty_bell = Slot_Game_Controller(self.ui, Liberty_Bell_Machine())
    self.menu = Menu_Controller(self.ui)
    self.view_items = View_Item_Controller(self.ui, Liberty_Bell_Machine())

    self._current_prog = self.liberty_bell
    self._current_prog.initialize_ui()

  def spin_pressed_handler(self, e=None):
    """ Handle the spin button """

    self._current_prog.spin_pressed_handler()

  def up_pressed_handler(self, e=None):
    """ Handle the up button """

    self._current_prog.up_pressed_handler()

  def down_pressed_handler(self, e=None):
    """ Handle the down button """

    self._current_prog.down_pressed_handler()

  def menu_pressed_handler(self, e=None):
    """ Handle the menu button """

    self._current_prog.menu_pressed_handler()

  def b1_pressed_handler(self, e=None):
    """ Handle the button """

    self._current_prog.b1_pressed_handler()

  def b2_pressed_handler(self, e=None):
    """ Handle the button """

    self._current_prog.b2_pressed_handler()

  def b3_pressed_handler(self, e=None):
    """ Handle the button """

    self._current_prog.b3_pressed_handler()

  def start(self):
    """ Start the program """

    while True:
      self.ui.detect_event()

      if self._current_prog.action == "liberty_bell":
        self._current_prog = self.liberty_bell
        self._current_prog.initialize_ui()

      if self._current_prog.action == "liberty_bell_auto":
        self._current_prog = self.liberty_bell
        self._current_prog.initialize_ui()
        self._current_prog.action = "autoplay"

      if self._current_prog.action == "autoplay":
        self.spin_pressed_handler()

      elif self._current_prog.action == 'menu':
        self._current_prog = self.menu
        self._current_prog.initialize_ui()

      elif self._current_prog.action == 'view_items':
        self._current_prog = self.view_items
        self._current_prog.initialize_ui()

      elif self._current_prog.action == "quit":
        sys.exit()

      time.sleep(0.1)
