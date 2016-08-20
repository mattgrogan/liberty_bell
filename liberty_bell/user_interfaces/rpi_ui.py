from __future__ import print_function

import random
import time
from datetime import datetime

import RPi.GPIO as GPIO
from button import Button
from liberty_bell.events import Events
from liberty_bell.ui import Slot_UI
from numeric_display import SevenSegment_Display, Text_Numeric_Display
from reel_display import SSD1351_Display, Text_Reel_Display

# import Adafruit_GPIO as GPIO

MENU_GPIO = 13

WINNER_PAID_LED = 0x71
CREDITS_LED = 0x72
AMOUNT_BET_LED = 0x70

SPIN_BUTTON_GPIO = 5
UP_BUTTON_GPIO = 14
DOWN_BUTTON_GPIO = 22

SPIN_BUTTON_LED = 4
DOWN_BUTTON_LED = 10
UP_BUTTON_LED = 19

REEL_BUTTON1_GPIO = 1
REEL_BUTTON1_LED = 0

REEL_BUTTON2_GPIO = 7
REEL_BUTTON2_LED = 11

REEL_BUTTON3_GPIO = 8
REEL_BUTTON3_LED = 9

# OLED
SSD1351_WIDTH = 128
SSD1351_HEIGHT = 128
RST = 24
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# Animation parameters
ROW_DELAY_LAMBDA = 0.001
ROW_DELAY_DIVISOR = 2


class Slot_RPI_UI(Slot_UI):
  """ Raspberry PI UI for the slot machine """

  def __init__(self, reels=None, **kwargs):
    """ Initialize the UI """

    super(Slot_RPI_UI, self).__init__(None, **kwargs)

    self.reels = reels
    self.current_stops = [0] * len(self.reels)

    # Set up the LEDs

    self.winner_paid_led = SevenSegment_Display(name="Winner Paid",
                                                address=WINNER_PAID_LED)
    self.credits_led = SevenSegment_Display(
        name="Credits", address=CREDITS_LED)

    self.amount_bet_led = SevenSegment_Display(
        name="Amount Bet", address=AMOUNT_BET_LED)

    # Set up the OLED screens
    self.display_1 = SSD1351_Display("Reel 1",
                                     SSD1351_WIDTH,
                                     SSD1351_HEIGHT,
                                     rst=25,
                                     dc=15,
                                     spi_port=1,
                                     spi_device=2)

    self.display_2 = SSD1351_Display("Reel 2",
                                     SSD1351_WIDTH,
                                     SSD1351_HEIGHT,
                                     rst=6,
                                     dc=26,
                                     spi_port=1,
                                     spi_device=1)

    self.display_3 = SSD1351_Display("Reel 3",
                                     SSD1351_WIDTH,
                                     SSD1351_HEIGHT,
                                     rst=24,
                                     dc=23,
                                     spi_port=1,
                                     spi_device=0)

    self.spin_button = Button("Spin", SPIN_BUTTON_GPIO, SPIN_BUTTON_LED)
    self.up_button = Button("Up", UP_BUTTON_GPIO, UP_BUTTON_LED)
    self.down_button = Button("Down", DOWN_BUTTON_GPIO, DOWN_BUTTON_LED)
    self.menu_button = Button("Menu", MENU_GPIO)

    self.reel1_button = Button("Reel 1", REEL_BUTTON1_GPIO, REEL_BUTTON1_LED)
    self.reel2_button = Button("Reel 2", REEL_BUTTON2_GPIO, REEL_BUTTON2_LED)
    self.reel3_button = Button("Reel 3", REEL_BUTTON3_GPIO, REEL_BUTTON3_LED)

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
