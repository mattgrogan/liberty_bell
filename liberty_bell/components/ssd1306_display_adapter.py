import time

from ssd1306_display import SSD1306_Display


class SSD1306_Display_Adapter(object):
  """ This wraps the SSD1306 """

  def __init__(self, name, width, height, rst, i2c_address):
    """ Initialize the  display """

    self.width = width
    self.height = height

    self._oled = SSD1306_Display(width, height, rst, i2c_address)

    self._oled.start_display()
    self._oled.clear_buffer()
    self._oled.write_buffer()

  def show_test_pattern(self):
    """ Display a basic test pattern """

    from PIL import Image, ImageDraw

    test_image = Image.new("1", (self.width, self.height))
    draw = ImageDraw.Draw(test_image)

    x_pos = 0
    x_offset = 8

    for bar in range(self.width / x_offset):
      color = 0xFF if bar % 2 == 0 else 0x00
      draw.rectangle((x_pos, 0, x_pos + x_offset, self.height),
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
