import random
import time

from components.button import Button
from components.numeric_display import SevenSegment_Display
from components.reel_display import SSD1351_Display
from config import Config

CONFIG_FILE = "config.ini"

# Animation parameters
ROW_DELAY_LAMBDA = 0.001
ROW_DELAY_DIVISOR = 2


class Slot_UI(object):
  """ UI for the slot machine """

  def __init__(self, reels):
    """ Initialize the UI """

    config = Config(CONFIG_FILE)

    # Set up events
    events = ["spin_pressed", "up_pressed", "down_pressed",
              "menu_pressed", "b1_pressed", "b2_pressed", "b3_pressed"]
    self.events = {event: dict() for event in events}

    self._numeric_displays = {}

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

    self.spin_button = Button("Spin", config.spin_pin, config.spin_led)
    self.up_button = Button("Up", config.up_pin, config.up_led)
    self.down_button = Button("Down", config.down_pin, config.down_led)
    self.menu_button = Button("Menu", config.menu_pin)

    self.reel1_button = Button("Btn 1", config.button1_pin, config.button1_led)
    self.reel2_button = Button("Btn 2", config.button2_pin, config.button2_led)
    self.reel3_button = Button("Btn 3", config.button3_pin, config.button3_led)

  def notify(self, event, message=None):
    """ Notify the subscribers for a particular event """

    for subscriber, callback in self.events[event].iteritems():
      callback(message)

  def register(self, event, who, callback=None):
    """ Register for updates """

    if callback is None:
      callback = getattr(who, 'update')

    self.events[event][who] = callback

  def startup_animation(self):
    """ Show some startup sequences """

    # Do nothing right now
    pass

  def mainloop(self):
    """ Wait for next button press """

    while True:

      if self.spin_button.event_detected:
        self.notify("spin_pressed")
      elif self.up_button.event_detected:
        self.notify("up_pressed")
      elif self.down_button.event_detected:
        self.notify("down_pressed")

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
    """ Animate the spin
    TODO: Remove spin animation logic from the ui object
    """

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
