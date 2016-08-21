
from __future__ import division

# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import math
import time

from PIL import Image, ImageDraw, ImageFont

import Adafruit_GPIO as GPIO
import Adafruit_GPIO.I2C as I2C

# Constants
SSD1306_SETCONTRAST = 0x81
SSD1306_DISPLAYALLON_RESUME = 0xA4
SSD1306_DISPLAYALLON = 0xA5
SSD1306_NORMALDISPLAY = 0xA6
SSD1306_INVERTDISPLAY = 0xA7
SSD1306_DISPLAYOFF = 0xAE
SSD1306_DISPLAYON = 0xAF
SSD1306_SETDISPLAYOFFSET = 0xD3
SSD1306_SETCOMPINS = 0xDA
SSD1306_SETVCOMDETECT = 0xDB
SSD1306_SETDISPLAYCLOCKDIV = 0xD5
SSD1306_SETPRECHARGE = 0xD9
SSD1306_SETMULTIPLEX = 0xA8
SSD1306_SETLOWCOLUMN = 0x00
SSD1306_SETHIGHCOLUMN = 0x10
SSD1306_SETSTARTLINE = 0x40
SSD1306_MEMORYMODE = 0x20
SSD1306_COLUMNADDR = 0x21
SSD1306_PAGEADDR = 0x22
SSD1306_COMSCANINC = 0xC0
SSD1306_COMSCANDEC = 0xC8
SSD1306_SEGREMAP = 0xA0
SSD1306_CHARGEPUMP = 0x8D
SSD1306_EXTERNALVCC = 0x1
SSD1306_SWITCHCAPVCC = 0x2

# Scrolling constants
SSD1306_ACTIVATE_SCROLL = 0x2F
SSD1306_DEACTIVATE_SCROLL = 0x2E
SSD1306_SET_VERTICAL_SCROLL_AREA = 0xA3
SSD1306_RIGHT_HORIZONTAL_SCROLL = 0x26
SSD1306_LEFT_HORIZONTAL_SCROLL = 0x27
SSD1306_VERTICAL_AND_RIGHT_HORIZONTAL_SCROLL = 0x29
SSD1306_VERTICAL_AND_LEFT_HORIZONTAL_SCROLL = 0x2A


class SSD1306_Display(object):

  def __init__(self, width, height, rst, i2c_address, gpio=None):

    self.width = width
    self.height = height

    self._pages = height // 8
    self._buffer = [0] * (width * self._pages)

    # Default to platform GPIO if not provided.
    self._gpio = gpio
    if self._gpio is None:
      self._gpio = GPIO.get_platform_gpio()
    # Setup reset pin.
    self._rst = rst
    self._gpio.setup(self._rst, GPIO.OUT)

    # Handle hardware I2C
    self._i2c = I2C.get_i2c_device(i2c_address)

  def _initialize(self):
    # 128x64 pixel specific initialization.
    self.send_command(SSD1306_DISPLAYOFF)                    # 0xAE
    self.send_command(SSD1306_SETDISPLAYCLOCKDIV)            # 0xD5
    # the suggested ratio 0x80
    self.send_command(0x80)
    self.send_command(SSD1306_SETMULTIPLEX)                  # 0xA8
    self.send_command(0x3F)
    self.send_command(SSD1306_SETDISPLAYOFFSET)              # 0xD3
    self.send_command(0x0)                                   # no offset
    self.send_command(SSD1306_SETSTARTLINE | 0x0)            # line #0
    self.send_command(SSD1306_CHARGEPUMP)                    # 0x8D
    if self._vccstate == SSD1306_EXTERNALVCC:
      self.send_command(0x10)
    else:
      self.send_command(0x14)
    self.send_command(SSD1306_MEMORYMODE)                    # 0x20
    # 0x0 act like ks0108
    self.send_command(0x00)
    self.send_command(SSD1306_SEGREMAP | 0x1)
    self.send_command(SSD1306_COMSCANDEC)
    self.send_command(SSD1306_SETCOMPINS)                    # 0xDA
    self.send_command(0x12)
    self.send_command(SSD1306_SETCONTRAST)                   # 0x81
    if self._vccstate == SSD1306_EXTERNALVCC:
      self.send_command(0x9F)
    else:
      self.send_command(0xCF)
    self.send_command(SSD1306_SETPRECHARGE)                  # 0xd9
    if self._vccstate == SSD1306_EXTERNALVCC:
      self.send_command(0x22)
    else:
      self.send_command(0xF1)
    self.send_command(SSD1306_SETVCOMDETECT)                 # 0xDB
    self.send_command(0x40)
    self.send_command(SSD1306_DISPLAYALLON_RESUME)           # 0xA4
    self.send_command(SSD1306_NORMALDISPLAY)                 # 0xA6

  def send_command(self, c):
    """Send command byte to display."""

    control = 0x00   # Co = 0, DC = 0
    self._i2c.write8(control, c)

  def send_data(self, c):
    """Send byte of data to display."""

    control = 0x40   # Co = 0, DC = 0
    self._i2c.write8(control, c)

  def start_display(self, vccstate=SSD1306_SWITCHCAPVCC):
    """Initialize display."""
    # Save vcc state.
    self._vccstate = vccstate
    # Reset and initialize display.
    self.reset()
    self._initialize()
    # Turn on the display.
    self.send_command(SSD1306_DISPLAYON)

  def reset(self):
    """Reset the display."""
    # Set reset high for a millisecond.
    self._gpio.set_high(self._rst)
    time.sleep(0.001)
    # Set reset low for 10 milliseconds.
    self._gpio.set_low(self._rst)
    time.sleep(0.010)
    # Set reset high again.
    self._gpio.set_high(self._rst)

  def write_buffer(self):
    """Write display buffer to physical display."""
    self.send_command(SSD1306_COLUMNADDR)
    self.send_command(0)              # Column start address. (0 = reset)
    self.send_command(self.width - 1)   # Column end address.
    self.send_command(SSD1306_PAGEADDR)
    self.send_command(0)              # Page start address. (0 = reset)
    self.send_command(self._pages - 1)  # Page end address.
    # Write buffer data.

    for i in range(0, len(self._buffer), 16):
      control = 0x40   # Co = 0, DC = 0
      self._i2c.writeList(control, self._buffer[i:i + 16])

  def load_image(self, image):
    """Set buffer to value of Python Imaging Library image.  The image should
    be in 1 bit mode and a size equal to the display size.
    """
    if image.mode != '1':
      raise ValueError('Image must be in mode 1.')
    imwidth, imheight = image.size
    if imwidth != self.width or imheight != self.height:
      raise ValueError('Image must be same dimensions as display ({0}x{1}).'
                       .format(self.width, self.height))
    # Grab all the pixels from the image, faster than getpixel.
    pix = image.load()
    # Iterate through the memory pages
    index = 0
    for page in range(self._pages):
      # Iterate through all x axis columns.
      for x in range(self.width):
        # Set the bits for the column of pixels at the current position.
        bits = 0
        # Don't use range here as it's a bit slow
        for bit in [0, 1, 2, 3, 4, 5, 6, 7]:
          bits = bits << 1
          bits |= 0 if pix[(x, page * 8 + 7 - bit)] == 0 else 1
        # Update buffer byte and increment to next byte.
        self._buffer[index] = bits
        index += 1

  def clear_buffer(self):
    """Clear contents of image buffer."""
    self._buffer = [0] * (self.width * self._pages)

  def set_contrast(self, contrast):
    """Sets the contrast of the display.  Contrast should be a value between
    0 and 255."""
    if contrast < 0 or contrast > 255:
      raise ValueError('Contrast must be a value from 0 to 255 (inclusive).')
    self.send_command(SSD1306_SETCONTRAST)
    self.send_command(contrast)
