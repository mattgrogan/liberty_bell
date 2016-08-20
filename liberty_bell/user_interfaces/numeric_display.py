""" This module holds the implementations for Seven Segment LEDs """

import time

TEST_DELAY_SECS = 1.0


class Numeric_Display(object):
  """ This object will display a numeric amount """

  def __init__(self):
    """ No initialization required """

    pass

  def clear(self):
    """ Clear the display """

    raise NotImplementedError("You must implement Numeric_Display.clear()")

  def display(self, value):
    """ Display the value """

    raise NotImplementedError("You must implement Numeric_Display.display()")

  def test(self):
    """ Show a test pattern """

    raise NotImplementedError("You must implement Numeric_Display.test()")


class Text_Numeric_Display(Numeric_Display):
  """ This class will output directly to the console """

  def __init__(self, name):
    """ Pass to the parent """

    self.name = name

  def clear(self):
    """ Do nothing """

    pass

  def display(self, val):
    """ Print the text """

    print "%s: %s\n" % (self.name, val)

  def test(self):
    """ Test the output """

    print "%s: test..." % self.name


class SevenSegment_Display(Numeric_Display):
  """ The Adafruit SevenSegment display """

  def __init__(self, name, address):
    """ Initalize a seven segment display with i2c """

    self.name = name
    self._address = address
    self._initialized = False

    from Adafruit_LED_Backpack import SevenSegment

    self._led = SevenSegment.SevenSegment(address=self._address)
    try:
      self._led.begin()
      self._initialized = True
    except IOError:
      msg = "Could not connect to %s LED at I2C address %s" % (
          self.name, hex(self._address))
      print(msg)
      # raise IOError("Could not connect to %s LED at I2C address %s" %
      #              (self.name, hex(self._address)))

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
