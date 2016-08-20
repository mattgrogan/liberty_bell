""" This module holds code for all displays """
import time

from ssd1351 import Adafruit_SSD1351

COLOR_BARS_PATH = "./icons/color_bars_128x128.gif"


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
    """ Show a test pattern with pause and clear """

    raise NotImplementedError("You must implement Reel_Display.test()")

  def show_test_pattern(self):
    """ Show a test pattern and leave it """

    raise NotImplementedError(
        "You must implement Reel_Display.show_test_pattern()")


class Text_Reel_Display():
  """ A basic text output for the reel result """

  def __init__(self, name):
    """ Initialize the display """

    self.name = name

  def show_test_pattern(self):
    """ We don't have a test pattern, pass """

    pass

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

  def show_test_pattern(self):
    """ Display the test bars """

    from PIL import Image, ImageDraw

    test_image = Image.new("RGB", (128, 128), "#000000")
    draw = ImageDraw.Draw(test_image)

    bar_colors = ["#FFFFFF",  # white
                  "#FFFF00",  # Yellow
                  "#00FFFF",  # Cyan
                  "#00FF00",  # Green
                  "#FF00FF",  # Magenta
                  "#FF0000",  # Red
                  "#000000",  # Black
                  "#0000FF"  # Blue
                  ]
    x_pos = 0
    x_offset = 16

    for color in bar_colors:

      draw.rectangle([(x_pos, 0), (x_pos + x_offset, 128)],
                     outline=color, fill=color)
      x_pos = x_pos + x_offset

    self._oled.load_image(test_image)
    self._oled.display()

  def test(self):
    """ Test the OLED """

    self.show_test_pattern()
    time.sleep(1)
    self.clear()

  def clear(self):
    """ Clear the display """

    self._oled.clear_buffer()
    self._oled.display()

  def display(self, data):
    """ Add row to the display """

    self._oled.display_scroll(data)
