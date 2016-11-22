import os
import textwrap
import time

from PIL import Image, ImageDraw, ImageFont

from liberty_bell.components.ssd1306_display import SSD1306_Display

dir = os.path.dirname(__file__)
#FONT_PATH = os.path.join(dir, '../fonts/VCR_OSD_MONO_1.001.ttf')
#FONT_PATH = os.path.join(dir, '../fonts/ARCADEPI.TTF')
FONT_PATH = os.path.join(dir, '../fonts/Moder DOS 437.ttf')
FONT_SIZE = 16

# liberty_bell\fonts\VCR_OSD_MONO_1.001.ttf


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

    self.clear()

  def show_test_pattern(self):
    """ Display a basic test pattern """

    self.clear()

    x_pos = 0
    x_offset = 8

    for bar in range(self.width / x_offset):
      color = 0xFF if bar % 2 == 0 else 0x00
      self.draw.rectangle((x_pos, 0, x_pos + x_offset, self.height),
                          outline=color, fill=color)
      x_pos = x_pos + x_offset

    self.display()

  def display(self):
    """ Write the image to the screen """

    self._oled.load_image(self.image)
    self._oled.write_buffer()

  def text(self, text, x=0, y=10, font_size=FONT_SIZE):
    """ Draw text on the screen """

    y_text = y

    font = ImageFont.truetype(FONT_PATH, font_size)
    lines = textwrap.wrap(text, width=14)

    for line in lines:
      width, height = font.getsize(line)
      self.draw.text((x, y_text), line, font=font, fill=255)
      y_text += height

  def test(self):
    """ Test the display """

    self.show_test_pattern()

  def clear(self):
    """ Clear the display """

    self.image = Image.new('1', (self.width, self.height))
    self.draw = ImageDraw.Draw(self.image)

    self._oled.clear_buffer()
    self._oled.write_buffer()
