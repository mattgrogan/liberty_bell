import itertools

from liberty_bell.slot_game_controller import Slot_Game_Controller
from liberty_bell.slot_machines import Liberty_Bell_Machine


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


class IP_Menu_Item(object):
  """ Shows the IP address """

  def __init__(self, text, ui, menu):
    """ Initialize """

    self.text = text
    self.ui = ui
    self.menu = menu

  def execute(self):
    """ Show the IP Address """

    import socket
    import fcntl
    import struct
    import time

    ifname = 'wlan0'

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip = socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

    self.ui.menu_display.clear()
    self.ui.menu_display.text(ip)
    self.ui.menu_display.display()

    time.sleep(2)

    return self.menu


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
    ip_menu_item = IP_Menu_Item("Show IP Address", self.ui, self)
    exit_item = Exit_Menu_Item()

    self.menu_items = [liberty_bell_item, ip_menu_item, exit_item]

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
