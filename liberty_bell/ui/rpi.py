from __future__ import division

import time

from components.button import Button
from components.buzzer import Buzzer
from components.numeric_display_adapter import Numeric_Display_Adapter
from components.ssd1306_display_adapter import SSD1306_Display_Adapter
from components.ssd1351_display_adapter import SSD1351_Display_Adapter
from config import Config


class Rpi_UI(object):

  def __init__(self, controller):

    self.controller = controller

    config = Config()

    # Set up the LEDs
    self.winner_paid_led = Numeric_Display_Adapter(
        name="Winner Paid", address=config.winner_paid_i2c)
    self.credits_led = Numeric_Display_Adapter(
        name="Credits", address=config.credits_i2c)
    self.amount_bet_led = Numeric_Display_Adapter(
        name="Amount Bet", address=config.amount_bet_i2c)

    self.menu_display = SSD1306_Display_Adapter(
        "Menu Display",
        config.menu_display_width,
        config.menu_display_height,
        config.menu_display_reset,
        config.menu_display_i2c)

    # Set up the OLED screens
    self.display_1 = SSD1351_Display_Adapter("Reel 1",
                                             config.display_1["width"],
                                             config.display_1["height"],
                                             config.display_1["reset"],
                                             config.display_1["dc"],
                                             config.display_1["spi_port"],
                                             config.display_1["spi_device"])

    self.display_2 = SSD1351_Display_Adapter("Reel 2",
                                             config.display_2["width"],
                                             config.display_2["height"],
                                             config.display_2["reset"],
                                             config.display_2["dc"],
                                             config.display_2["spi_port"],
                                             config.display_2["spi_device"])

    self.display_3 = SSD1351_Display_Adapter("Reel 3",
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

    self.buzzer = Buzzer(config.buzzer_pin, config.sound_enabled)

  def detect_event(self):
    """ Detect button presses """
    # TODO: Use callbacks instead of polling

    if self.spin_button.event_detected:
      self.controller.handle_spin()
    elif self.up_button.event_detected:
      self.controller.handle_up()
    elif self.down_button.event_detected:
      self.controller.handle_down()
    elif self.menu_button.event_detected:
      self.controller.handle_menu()
    elif self.reel1_button.event_detected:
      self.controller.handle_b1()
    elif self.reel2_button.event_detected:
      self.controller.handle_b2()
    elif self.reel3_button.event_detected:
      self.controller.handle_b3()

  def mainloop(self):

    while True:
      self.detect_event()
      self.controller.run()
      time.sleep(0.1)
