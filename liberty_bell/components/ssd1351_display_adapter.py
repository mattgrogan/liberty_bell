""" This module holds code for all displays """
import time

from ssd1351_display import SSD1351_Display


class SSD1351_Display_Adapter(object):
  """ This wraps the SSD1351 """

  def __init__(self, name, width, height, rst, dc, spi_port, spi_device):
    """ Initialze the display """

    self.width = width
    self.height = height
    self._oled = SSD1351_Display(
        width, height, rst=rst, dc=dc, spi_port=spi_port, spi_device=spi_device)

    self._oled.start_display()
    self._oled.clear_buffer()

  def display_image(self, image):
    """ Load an image into the buffer """

    self._oled.load_image(image)
    self._oled.write_buffer()

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
    self._oled.write_buffer()

  def test(self):
    """ Test the display """

    self.show_test_pattern()

  def clear(self):
    """ Clear the display """

    self._oled.clear_buffer()
    self._oled.write_buffer()

  def write_line(self, data):
    """ Add row to the display """

    color_data = []

    for pixel in data:
      r, g, b = pixel
      color_data.append(color565(r, g, b))

    self._oled.write_line(color_data)


def color565(red, green=None, blue=None):
  """ Define color in 16-bit RGB565. Red and blue
  have five bits each and green has 6 (since the
  eye is more sensitive to green).

  Bit Format: RRRR RGGG GGGB BBBB

  Usage:
  color565(red=[0,255], green=[0,255], blue=[0,255])
  color565(0xFFE92)
  """

  if green is None and blue is None:
        # We were passed the full value in the first argument
    hexcolor = red
    red = (hexcolor >> 16) & 0xFF
    green = (hexcolor >> 8) & 0xFF
    blue = hexcolor & 0xFF

  # We have 8 bits coming in 0-255
  # So we truncate the least significant bits
  # until there's 5 bits for red and blue
  # and six for green
  red >>= 3
  green >>= 2
  blue >>= 3

  # Now move them to the correct locations
  red <<= 11
  green <<= 5

  # Then "or" them together
  result = red | green | blue

  return result
