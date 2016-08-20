""" This module holds the implementations for Seven Segment LEDs """
import time

from Adafruit_LED_Backpack import SevenSegment

TEST_DELAY_SECS = 1.0


class SevenSegment_Display(object):
  """ The Adafruit SevenSegment display """

  def __init__(self, name, address):
    """ Initalize a seven segment display with i2c """

    self.name = name
    self._address = address
    self._initialized = False

    self._led = SevenSegment.SevenSegment(address=self._address)
    try:
      self._led.begin()
      self.clear()
      self._initialized = True
    except IOError:
      msg = "Could not connect to %s LED at I2C address %s" % (
          self.name, hex(self._address))
      print(msg)

  def clear(self):
    """ Clear the display """

    self._led.clear()
    self._led.write_display()

  def display(self, val):
    """ Display value """

    self._led.clear()
    self._led.print_float(val, decimal_digits=0)
    self._led.write_display()

  def test(self, reps=2, timeout=TEST_DELAY_SECS):
    """ Show a test pattern on the display """

    if not self._initialized:
      print("Not connected to %s LED at I2c address %s" %
            (self.name, hex(self._address)))
      return

    for i in range(reps):

      self.clear()
      time.sleep(timeout / 2)

      self.display(8888)
      time.sleep(timeout / 2)

      self.clear()
