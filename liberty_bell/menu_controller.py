import itertools


class Menu_Item(object):
  """ Holds a menu item """

  def __init__(self, name, text):
    """ Initialize the menu item """

    self.name = name
    self.text = text


class Menu_Controller(object):
  """ Handles all menu options """

  def __init__(self, ui):
    """ Initialize the menu """

    self.ui = ui

    liberty_bell_item = Menu_Item(
        name="liberty_bell", text="Play Liberty Bell")
    liberty_bell_auto = Menu_Item(
        name="liberty_bell_auto", text="Play Liberty Bell (autoplay)")
    view_items = Menu_Item(name="view_items", text="View Items")
    quit_item = Menu_Item(name="quit", text="Quit")

    self.menu_items = [liberty_bell_item,
                       liberty_bell_auto, view_items, quit_item]

    self._menu_items = itertools.cycle(self.menu_items)
    self._current_item = self._menu_items.next()
    self.action = None

  def initialize_ui(self):
    """ Set up the UI """

    self.ui.spin_button.enable()
    self.ui.up_button.disable()
    self.ui.down_button.disable()
    self.ui.reel1_button.disable()
    self.ui.reel2_button.disable()
    self.ui.reel3_button.disable()

    self.ui.credits_led.clear()
    self.ui.winner_paid_led.clear()
    self.ui.amount_bet_led.clear()

    self.action = None
    self._menu_items = itertools.cycle(self.menu_items)
    self._current_item = self._menu_items.next()
    self.display()

    self.ui.display_1.clear()
    self.ui.display_2.clear()
    self.ui.display_3.clear()

  def menu_pressed_handler(self, message=None):
    """ Show the next menu option """

    self.action = None
    self._current_item = self._menu_items.next()
    self.display()

  def spin_pressed_handler(self, message=None):
    """ User selected this item """

    # Action is queried by application controller
    self.action = self._current_item.name

  def display(self):
    """ Display a menu item """

    self.ui.menu_display.clear()
    self.ui.menu_display.text(self._current_item.text)
    self.ui.menu_display.display()
