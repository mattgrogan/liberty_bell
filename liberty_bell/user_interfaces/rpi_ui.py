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

#import Adafruit_GPIO as GPIO

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

REEL_BUTTON1_GPIO = 8
REEL_BUTTON1_LED = 9

REEL_BUTTON2_GPIO = 7
REEL_BUTTON2_LED = 11

REEL_BUTTON3_GPIO = 1
REEL_BUTTON3_LED = 0

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

    winner_paid_led = SevenSegment_Display(name="Winner Paid",
                                                address=WINNER_PAID_LED)
    winner_paid_text = Text_Numeric_Display(name="Winner Paid")

    self.add_numeric_display("Winner Paid", winner_paid_led)
    self.add_numeric_display("Winner Paid", winner_paid_text)

    credits_led = SevenSegment_Display(
        name="Credits", address=CREDITS_LED)
    credits_text = Text_Numeric_Display(name="Credits")
    self.add_numeric_display("Credits", credits_led)
    self.add_numeric_display("Credits", credits_text)

    amount_bet_led = SevenSegment_Display(
        name="Amount Bet", address=AMOUNT_BET_LED)
    amount_bet_text = Text_Numeric_Display(name="Amount Bet")
    self.add_numeric_display("Amount Bet", amount_bet_led)
    self.add_numeric_display("Amount Bet", amount_bet_text)

    # Set up the OLED screens

    reel0_oled = SSD1351_Display("Reel 1",
                                 SSD1351_WIDTH,
                                 SSD1351_HEIGHT,
                                 rst=25,
                                 dc=15,
                                 spi_port=1,
                                 spi_device=2)

    reel1_oled = SSD1351_Display("Reel 2",
                                 SSD1351_WIDTH,
                                 SSD1351_HEIGHT,
                                 rst=6,
                                 dc=26,
                                 spi_port=1,
                                 spi_device=1)

    reel2_oled = SSD1351_Display("Reel 3",
                                 SSD1351_WIDTH,
                                 SSD1351_HEIGHT,
                                 rst=24,
                                 dc=23,
                                 spi_port=1,
                                 spi_device=0)

    reel0_text = Text_Reel_Display("Reel 1")
    reel1_text = Text_Reel_Display("Reel 2")
    reel2_text = Text_Reel_Display("Reel 3")

    self.add_reel_display("Reel 1", reel0_oled)
    self.add_reel_display("Reel 1", reel0_text)
    self.add_reel_display("Reel 2", reel1_oled)
    self.add_reel_display("Reel 2", reel1_text)
    self.add_reel_display("Reel 3", reel2_oled)
    self.add_reel_display("Reel 3", reel2_text)

    self.spin_button = Button("Spin", SPIN_BUTTON_GPIO, SPIN_BUTTON_LED)

    #self.add_button(Button("Spin", SPIN_BUTTON_GPIO, SPIN_BUTTON_LED))
    self.add_button(Button("Up", UP_BUTTON_GPIO, UP_BUTTON_LED))
    self.add_button(Button("Down", DOWN_BUTTON_GPIO, DOWN_BUTTON_LED))

    self.add_button(Button("Reel 1", REEL_BUTTON1_GPIO, REEL_BUTTON1_LED))
    self.add_button(Button("Reel 2", REEL_BUTTON2_GPIO, REEL_BUTTON2_LED))
    self.add_button(Button("Reel 3", REEL_BUTTON3_GPIO, REEL_BUTTON3_LED))

    self.add_button(Button("Menu", MENU_GPIO))

  def startup_animation(self):
    """ Show some startup sequences """

    # Display test pattern on the oleds
    for reel in self.reels:
      self.show_test_pattern(reel.name)

  def listen_for_input(self):
    """ Wait for next button press """

    while True:

      if self.spin_button.event_detected:
        self.on_spin_press()
      elif self.button_pressed("Up"):
        self.on_up_press()
      elif self.button_pressed("Down"):
        self.on_down_press()

      time.sleep(0.01)

  def on_spin_press(self, e=None):
    """ Notify observers that the button was pressed """

    self.notify(Events.SPIN)

  def on_up_press(self, e=None):
    """ Notify observers that the button was pressed """

    self.notify(Events.INCREMENT_BET)

  def on_down_press(self, e=None):
    """ Notify observers that the button was pressed """

    self.notify(Events.DECREMENT_BET)

  def update_credits(self, credits):
    """ Update the credits box """

    self.update_numeric_display("Credits", credits)

  def update_bet(self, bet):
    """ Update the bet """

    self.update_numeric_display("Amount Bet", bet)

  def update_winner_paid(self, winner_paid):
    """ Print the amount paid """

    self.update_numeric_display("Winner Paid", winner_paid)

  def clear_winner_paid(self):
    """ Blank out the winner paid amount """

    self.clear_numeric_display("Winner Paid")

  def test(self):
    """ Test the UI elements """

    for button in self.buttons:
      self.buttons[button].test()

    self.test_numeric_display("Credits")
    self.test_numeric_display("Amount Bet")
    self.test_numeric_display("Winner Paid")

    for reel in self.reels:
      self.test_reel_display(reel.name)

  def show_spin(self, result):
    """ Animate the spin """

    # Print the reels to the screen
    for i, reel in enumerate(result.reels):
      print("Reel %i: %s" % (i, reel))

    # Which reels are still spinning?
    reel_iterators = []

    for i, reel in enumerate(self.reels):
      # Get an iterator
      required_spins = ((i + 1) ** 2)
      reel_iterator = reel.get_scroller(
          result.reels[i], required_spins=required_spins)
      reel_iterators.append(reel_iterator)

    while len(reel_iterators) >= 1:
      for i, reel in enumerate(reel_iterators):

        try:
          line = reel.next()
          self.update_reel_display(reel.slot_reel.name, line)
          # slow down the reels
          delay = random.expovariate(1 / ROW_DELAY_LAMBDA) / \
              ((len(reel_iterators) + 1) * ROW_DELAY_DIVISOR)
          time.sleep(delay)
        except StopIteration:
          reel_iterators.remove(reel)
