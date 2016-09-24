import itertools

from slot_game_controller import Slot_Game_Controller
from slot_machines import Liberty_Bell_Machine


class Slot_Machine_Menu_Item(object):
  """ Run a slot machine """

  def __init__(self, text, ui, slot_machine):
    """ Initialize the menu option """

    self.text = text
    self.ui = ui
    self.slot_machine = slot_machine
    self.controller = Slot_Game_Controller(self.ui, self.slot_machine)

  def execute(self):
    """ Return the slot machine """

    return self.controller


class Exit_Menu_Item(object):
  """ Exit the game """

  def __init__(self):
    """ Initialize the menu item """

    self.text = "Exit"

  def execute(self):
    """ Quit the application """
    import sys
    sys.exit()


class Menu_Controller(object):
  """ Handles all menu options """

  def __init__(self, ui):
    """ Initialize the menu """

    self.ui = ui

    liberty_bell_item = Slot_Machine_Menu_Item(
        "Play Liberty Bell", self.ui, Liberty_Bell_Machine())
    exit_item = Exit_Menu_Item()

    self.menu_items = [liberty_bell_item, exit_item]

    self._menu_items = itertools.cycle(self.menu_items)
    self._current_item = self._menu_items.next()

  def initialize_ui(self):
    """ Set up the UI """

    # Down button moves to next item
    self.ui.menu_button.enable()
    self.ui.down_button.enable()

    self.ui.spin_button.disable()
    self.ui.up_button.disable()
    self.ui.reel1_button.disable()
    self.ui.reel2_button.disable()
    self.ui.reel3_button.disable()

    self.ui.credits_led.clear()
    self.ui.winner_paid_led.clear()
    self.ui.amount_bet_led.clear()

    self._menu_items = itertools.cycle(self.menu_items)
    self._current_item = self._menu_items.next()
    self.display()

    self.ui.display_1.clear()
    self.ui.display_2.clear()
    self.ui.display_3.clear()

  def menu_pressed_handler(self, message=None):
    """ User selected this menu option """

    return self._current_item.execute()

  def down_pressed_handler(self, message=None):
    """ Move to next item """

    self._current_item = self._menu_items.next()
    self.display()

  def display(self):
    """ Display a menu item """

    self.ui.menu_display.clear()
    self.ui.menu_display.text(self._current_item.text)
    self.ui.menu_display.display()
