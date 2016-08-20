from __future__ import print_function

import ConfigParser
import random
import time
from datetime import datetime

import RPi.GPIO as GPIO
from button import Button
from liberty_bell.events import Events
from liberty_bell.ui import Slot_UI
from numeric_display import SevenSegment_Display
from reel_display import SSD1351_Display

# import Adafruit_GPIO as GPIO
CONFIG_FILE = "config.ini"

# Animation parameters
ROW_DELAY_LAMBDA = 0.001
ROW_DELAY_DIVISOR = 2


class Slot_Config(object):
  """ Handle all the configuration options """

  def __init__(self, config_file):
    """ Read the configuration file and parse out the options """

    config = ConfigParser.ConfigParser()
    config.read(config_file)
    self.config = config

    # SEVEN SEGMENT DISPLAYS
    self.winner_paid_i2c = config.get("SEVENSEG_DISPLAYS", "winner_paid_i2c")
    self.credits_i2c = config.get("SEVENSEG_DISPLAYS", "credits_i2c")
    self.amount_bet_i2c = config.get("SEVENSEG_DISPLAYS", "amount_bet_i2c")

    # Convert to hex
    self.winner_paid_i2c = int(self.winner_paid_i2c, 16)
    self.credits_i2c = int(self.credits_i2c, 16)
    self.amount_bet_i2c = int(self.amount_bet_i2c, 16)

    # BUTTON GPIO PINS
    self.spin_button_pin = config.getint("BUTTON_PINS", "spin_button_pin")
    self.up_button_pin = config.getint("BUTTON_PINS", "up_button_pin")
    self.down_button_pin = config.getint("BUTTON_PINS", "down_button_pin")
    self.button1_pin = config.getint("BUTTON_PINS", "button1_pin")
    self.button2_pin = config.getint("BUTTON_PINS", "button2_pin")
    self.button3_pin = config.getint("BUTTON_PINS", "button3_pin")
    self.menu_button_pin = config.getint("BUTTON_PINS", "menu_button_pin")

    # BUTTON LED PINS
    self.spin_button_led = config.getint("BUTTON_LEDS", "spin_button_led")
    self.up_button_led = config.getint("BUTTON_LEDS", "up_button_led")
    self.down_button_led = config.getint("BUTTON_LEDS", "down_button_led")
    self.button1_led = config.getint("BUTTON_LEDS", "button1_led")
    self.button2_led = config.getint("BUTTON_LEDS", "button2_led")
    self.button3_led = config.getint("BUTTON_LEDS", "button3_led")

    # DISPLAYS
    self.display_1 = self.get_section_dict("DISPLAY_1")
    self.display_2 = self.get_section_dict("DISPLAY_2")
    self.display_3 = self.get_section_dict("DISPLAY_3")

  def get_section_dict(self, section):
    """ Read in a sectiion as a dict """

    result = {}

    for opt in self.config.options(section):
      result[opt] = self.config.getint(section, opt)

    return result


class Slot_RPI_UI(Slot_UI):
  """ Raspberry PI UI for the slot machine """

  def __init__(self, reels=None, **kwargs):
    """ Initialize the UI """

    super(Slot_RPI_UI, self).__init__(None, **kwargs)

    config = Slot_Config(CONFIG_FILE)

    self.reels = reels
    self.current_stops = [0] * len(self.reels)

    # Set up the LEDs
    self.winner_paid_led = SevenSegment_Display(
        name="Winner Paid", address=config.winner_paid_i2c)
    self.credits_led = SevenSegment_Display(
        name="Credits", address=config.credits_i2c)
    self.amount_bet_led = SevenSegment_Display(
        name="Amount Bet", address=config.amount_bet_i2c)

    # Set up the OLED screens
    self.display_1 = SSD1351_Display("Reel 1",
                                     config.display_1["width"],
                                     config.display_1["height"],
                                     config.display_1["reset"],
                                     config.display_1["dc"],
                                     config.display_1["spi_port"],
                                     config.display_1["spi_device"])

    self.display_2 = SSD1351_Display("Reel 2",
                                     config.display_2["width"],
                                     config.display_2["height"],
                                     config.display_2["reset"],
                                     config.display_2["dc"],
                                     config.display_2["spi_port"],
                                     config.display_2["spi_device"])

    self.display_3 = SSD1351_Display("Reel 3",
                                     config.display_3["width"],
                                     config.display_3["height"],
                                     config.display_3["reset"],
                                     config.display_3["dc"],
                                     config.display_3["spi_port"],
                                     config.display_3["spi_device"])

    self.spin_button = Button(
        "Spin", config.spin_button_pin, config.spin_button_led)
    self.up_button = Button("Up", config.up_button_pin, config.up_button_led)
    self.down_button = Button(
        "Down", config.down_button_pin, config.down_button_led)
    self.menu_button = Button("Menu", config.menu_button_pin)

    self.reel1_button = Button(
        "Reel 1", config.button1_pin, config.button1_led)
    self.reel2_button = Button(
        "Reel 2", config.button2_pin, config.button2_led)
    self.reel3_button = Button(
        "Reel 3", config.button3_pin, config.button3_led)

  def startup_animation(self):
    """ Show some startup sequences """

    # Do nothing right now
    pass

  def listen_for_input(self):
    """ Wait for next button press """

    while True:

      if self.spin_button.event_detected:
        self.notify(Events.SPIN)
      elif self.up_button.event_detected:
        self.notify(Events.INCREMENT_BET)
      elif self.down_button.event_detected:
        self.notify(Events.DECREMENT_BET)

      time.sleep(0.01)

  def test(self):
    """ Test the UI elements """

    self.spin_button.test()
    self.up_button.test()
    self.down_button.test()
    self.menu_button.test()

    self.credits_led.test()
    self.winner_paid_led.test()
    self.amount_bet_led.test()

    self.display_1.test()
    self.display_2.test()
    self.display_3.test()

    self.reel1_button.test()
    self.reel2_button.test()
    self.reel3_button.test()

  def show_spin(self, result):
    """ Animate the spin """

    # Print the reels to the screen
    for i, reel in enumerate(result.reels):
      print("Reel %i: %s" % (i, reel))

    # Which reels are still spinning?
    reel_iterators = []

    iter0 = self.reels[0].get_scroller(result.reels[0], required_spins=1)
    iter1 = self.reels[1].get_scroller(result.reels[1], required_spins=2)
    iter2 = self.reels[2].get_scroller(result.reels[2], required_spins=4)

    reel_iterators.append((iter0, self.display_1))
    reel_iterators.append((iter1, self.display_2))
    reel_iterators.append((iter2, self.display_3))

    while len(reel_iterators) >= 1:
      for reel, display in reel_iterators:

        try:
          line = reel.next()
          display.display(line)
          # slow down the reels
          delay = random.expovariate(1 / ROW_DELAY_LAMBDA) / \
              ((len(reel_iterators) + 1) * ROW_DELAY_DIVISOR)
          time.sleep(delay)
        except StopIteration:
          reel_iterators.remove((reel, display))
