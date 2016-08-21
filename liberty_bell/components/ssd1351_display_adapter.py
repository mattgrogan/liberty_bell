""" This module holds code for all displays """
import time

from ssd1351 import SSD1351_Display


class SSD1351_Display_Adapter(object):
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
    """ Test the display """

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
