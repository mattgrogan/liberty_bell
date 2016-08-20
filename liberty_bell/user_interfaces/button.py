from __future__ import print_function

import sys
import time

import RPi.GPIO as gpio


class Button(object):
  """ Represent a physical button """

  def __init__(self, name, gpio_pin, led_pin=None):
    """ Initialize the button with a specific gpio pin """

    self.name = name
    self.gpio_pin = gpio_pin
    self.led_pin = led_pin

    # Set up the GPIO pins
    gpio.setmode(gpio.BCM)
    gpio.setup(gpio_pin, gpio.IN, pull_up_down=gpio.PUD_UP)

    if self.led_pin is not None:
      gpio.setup(self.led_pin, gpio.OUT)

  def led_on(self):
    """ Turn the LED on """

    if self.led_pin is not None:
      gpio.output(self.led_pin, gpio.HIGH)

  def led_off(self):
    """ Turn the LED off """

    if self.led_pin is not None:
      gpio.output(self.led_pin, gpio.LOW)

  def led_toggle(self):
    """ Switch the LED """

    if self.led_pin is not None:
      gpio.output(self.led_pin, not gpio.input(self.led_pin))

  def enable(self):
    """ Begin listening to events """

    gpio.add_event_detect(self.gpio_pin, gpio.RISING, bouncetime=500)

  def disable(self):
    """ Stop listening to events """

    gpio.remove_event_detect(self.gpio_pin)

  @property
  def event_detected(self):
    """ Return true if the gpio event was detected """

    return gpio.event_detected(self.gpio_pin)

  def test(self, timeout=10):
    """ Test the button """

    self.enable()
    print("Press %s on pin %i within %i seconds" %
          (self.name, self.gpio_pin, timeout))

    for t in range(timeout):
      if self.event_detected:
        print("Click detected!")
        self.led_off()
        return True
      else:
        sys.stdout.write('.')
        sys.stdout.flush()
        self.led_toggle()
        time.sleep(1)

    print("Button %s failed." % self.name)
    self.led_off()
    return False
