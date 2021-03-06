from __future__ import division

import pygame
from pygame.locals import *

import RPi.GPIO as gpio
from liberty_bell.components.button import Button
from liberty_bell.components.buzzer import Buzzer
from liberty_bell.components.numeric_display_adapter import \
    Numeric_Display_Adapter
from liberty_bell.config import Config


class Rpi_UI(object):

    def __init__(self):

        pass

    def initialize(self, callback):
        self.callback = callback

        config = Config()

        # Set up the LEDs
        self.winner_paid_led = Numeric_Display_Adapter(
            name="Winner Paid", address=config.winner_paid_i2c)
        self.credits_led = Numeric_Display_Adapter(
            name="Credits", address=config.credits_i2c)
        self.amount_bet_led = Numeric_Display_Adapter(
            name="Amount Bet", address=config.amount_bet_i2c)



        self.spin_button = Button("Spin", config.spin_pin, config.spin_led)
        self.up_button = Button("Up", config.up_pin, config.up_led)
        self.down_button = Button("Down", config.down_pin, config.down_led)
        self.menu_button = Button("Menu", config.menu_pin)

        self.reel1_button = Button(
            "Btn 1", config.button1_pin, config.button1_led)
        self.reel2_button = Button(
            "Btn 2", config.button2_pin, config.button2_led)
        self.reel3_button = Button(
            "Btn 3", config.button3_pin, config.button3_led)

        self.buzzer = Buzzer(config.buzzer_pin, config.sound_enabled)

    def shutdown(self):
        """ Turn everything off """

        for display in self.reel_displays:
            display.clear()

        self.menu_display_driver.clear()

        self.amount_bet_led.clear()
        self.winner_paid_led.clear()
        self.credits_led.clear()

        gpio.cleanup()

    def detect_event(self):
        """ Detect button presses """
        # TODO: Use callbacks instead of polling

        if self.spin_button.event_detected:
            self.callback("SPIN")
        elif self.up_button.event_detected:
            self.callback("UP")
        elif self.down_button.event_detected:
            self.callback("DOWN")
        elif self.menu_button.event_detected:
            self.callback("MENU")
        elif self.reel1_button.event_detected:
            self.callback("B1")
        elif self.reel2_button.event_detected:
            self.callback("B2")
        elif self.reel3_button.event_detected:
            self.callback("B3")

    def ready(self):
        self.detect_event()
        #self.run_callback()

    def schedule_next(self, requested_delay_ms):
        time.sleep(requested_delay_ms * 0.001)
        self.detect_event()
        #self.run_callback()

    def update(self):
        pass
