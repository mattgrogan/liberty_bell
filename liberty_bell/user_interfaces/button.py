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

  def enable(self):
    """ Begin listening to events """

    gpio.add_event_detect(self.gpio_pin, gpio.RISING)

  def disable(self):
    """ Stop listening to events """

    gpio.remove_event_detect(self.gpio_pin)

  @property
  def event_detected(self):
    """ Return true if the gpio event was detected """

    return gpio.event_detected(self.gpio_pin)
