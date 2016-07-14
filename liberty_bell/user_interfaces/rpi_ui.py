from __future__ import print_function

import random
import time
from datetime import datetime

import RPi.GPIO as GPIO
from Adafruit_LED_Backpack import SevenSegment
from button import Button
from liberty_bell.events import Events
from liberty_bell.ui import Slot_UI
from ssd1351 import Adafruit_SSD1351

WINNER_PAID_LED = 0x70
CREDITS_LED = 0x71
AMOUNT_BET_LED = 0x72

SPIN_BUTTON_GPIO = 18

# OLED
SSD1351_WIDTH = 128
SSD1351_HEIGHT = 128
RST = 24
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0


class Slot_RPI_UI(Slot_UI):
  """ Raspberry PI UI for the slot machine """

  def __init__(self, reels=None, **kwargs):
    """ Initialize the UI """

    super(Slot_RPI_UI, self).__init__(None, **kwargs)

    self.reels = reels
    self.current_stops = [0] * len(self.reels)

    # Set up the winner paid LED
    self.winner_paid_led = SevenSegment.SevenSegment(
        address=WINNER_PAID_LED)
    self.winner_paid_led.begin()
    self.winner_paid_led.clear()
    self.winner_paid_led.write_display()

    # Set up the credits LED
    self.credits_led = SevenSegment.SevenSegment(address=CREDITS_LED)
    self.credits_led.begin()
    self.credits_led.clear()
    self.credits_led.write_display()

    # Set up the amount bet LED
    self.amount_bet_led = SevenSegment.SevenSegment(address=AMOUNT_BET_LED)
    self.amount_bet_led.begin()
    self.amount_bet_led.clear()
    self.amount_bet_led.write_display()

    # Set up the OLED screens
    self.oleds = []

    self.oleds.append(Adafruit_SSD1351(SSD1351_WIDTH,
                                       SSD1351_HEIGHT,
                                       rst=25,
                                       dc=26,
                                       spi_port=1,
                                       spi_device=0))

    self.oleds.append(Adafruit_SSD1351(SSD1351_WIDTH,
                                       SSD1351_HEIGHT,
                                       rst=14,
                                       dc=15,
                                       spi_port=SPI_PORT,
                                       spi_device=1))

    self.oleds.append(Adafruit_SSD1351(SSD1351_WIDTH,
                                       SSD1351_HEIGHT,
                                       rst=RST,
                                       dc=DC,
                                       spi_port=SPI_PORT,
                                       spi_device=SPI_DEVICE))

    self.oleds[0].begin()
    self.oleds[0].clear_buffer()
    self.oleds[0].display()

    self.oleds[1].begin()
    self.oleds[1].clear_buffer()
    self.oleds[1].display()

    self.oleds[2].begin()
    self.oleds[2].clear_buffer()
    self.oleds[2].display()

    self.spin_button = Button("Spin", SPIN_BUTTON_GPIO)

  def enable_spin_button(self):
    """ Enable the spin button """

    self.spin_button.enable()

  def disable_spin_button(self):
    """ Disable the spin button """

    self.spin_button.disable()

  def listen_for_input(self):
    """ Wait for next button press """

    while True:
      if self.spin_button.event_detected:
        self.on_spin_press()
      time.sleep(0.01)

  def on_spin_press(self, e=None):
    """ Notify observers that the button was pressed """

    self.notify(Events.SPIN)

  def update_credits(self, credits):
    """ Update the credits box """

    print("Credits: %i" % credits)
    self.credits_led.clear()
    self.credits_led.print_float(credits, decimal_digits=0)
    self.credits_led.write_display()

  def update_bet(self, bet):
    """ Update the bet """

    print("Bet: %i" % bet)
    self.amount_bet_led.clear()
    self.amount_bet_led.print_float(bet, decimal_digits=0)
    self.amount_bet_led.write_display()

  def update_winner_paid(self, winner_paid):
    """ Print the amount paid """

    print("Winner paid: %i" % winner_paid)
    self.winner_paid_led.clear()
    self.winner_paid_led.print_float(winner_paid, decimal_digits=0)
    self.winner_paid_led.write_display()

  def clear_winner_paid(self):
    """ Blank out the winner paid amount """

    self.winner_paid_led.clear()
    self.winner_paid_led.write_display()

  def show_spin(self, result):
    """ Animate the spin """

    # Print the reels to the screen
    for i, reel in enumerate(result.reels):
      print("Reel %i: %s" % (i, reel))

    # Reset the reels
    for reel in range(len(self.reels)):
      self.reels[reel].reset(required_spins=((reel + 1) ** 2))

    # Which reels are still spinning?
    reel_iterators = []

    for i, reel in enumerate(self.reels):
      # Get an iterator
      reel_iterator = reel.get_scroller(result.reels[i])
      reel_iterators.append(reel_iterator)

    while len(reel_iterators) >= 1:
      for i, reel in enumerate(reel_iterators):

        try:
          line = reel.next()
          self.oleds[reel.slot_reel.index].display_scroll(line)
        except StopIteration:
          reel_iterators.remove(reel)
