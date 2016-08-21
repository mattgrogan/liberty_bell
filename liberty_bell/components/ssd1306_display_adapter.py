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

    from PIL import Image, ImageDraw, ImageFont

    test_image = Image.new("1", (self.width, self.height))
    draw = ImageDraw.Draw(test_image)
    font = ImageFont.load_default()

    draw.text((20, 20), 'Liberty Bell',  font=font, fill=255)

    self._oled.load_image(test_image)
    self._oled.write_buffer()

  def test(self):
    """ Test the display """

    self.show_test_pattern()
    time.sleep(1)
    self.clear()

  def clear(self):
    """ Clear the display """

    self._oled.clear_buffer()
    self._oled.write_buffer()
