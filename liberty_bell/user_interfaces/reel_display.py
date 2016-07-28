""" This module holds code for all displays """
import time

from ssd1351 import Adafruit_SSD1351


class Reel_Display(object):
  """ Represent a  display that shows results on a reel """

  def __init__(self):
    """ No initialization required """

    pass

  def clear(self):
    """ Clear the display """

    raise NotImplementedError("You must implement Reel_Display.clear()")

  def display(self):
    """ Display image on the display """

    raise NotImplementedError("You must implement Reel_Display.display()")

  def test(self):
    """ Show a test pattern """

    raise NotImplementedError("You must implement Reel_Display.test()")


class Text_Reel_Display():
  """ A basic text output for the reel result """

  def __init__(self, name):
    """ Initialize the display """

    self.name = name

  def test(self):
    """ Test the display """

    print "%s: test" % self.name

  def clear(self):
    """ Clear on text does nothing """

    pass

  def display(self, data):
    """ Display some output """

    pass


class SSD1351_Display(Reel_Display):
  """ This wraps the SSD1351 """

  def __init__(self, name, width, height, rst, dc, spi_port, spi_device):
    """ Initialze the display """

    self.width = width
    self.height = height
    self._oled = Adafruit_SSD1351(
        width, height, rst=rst, dc=dc, spi_port=spi_port, spi_device=spi_device)

    self._oled.begin()
    self._oled.clear_buffer()

  def test(self):
    """ Test the OLED """

    self._oled.rawfill(0, 0, self.width, self.height, 0x1B6DEF)
    time.sleep(1)
    self.clear()

  def clear(self):
    """ Clear the display """

    self._oled.clear_buffer()
    self._oled.display()

  def display(self, data):
    """ Add row to the display """

    self._oled.display_scroll(data)
