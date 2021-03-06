#import glob
#import random
import time

from PIL import Image, ImageDraw, ImageFont, ImageOps

import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI

# SSD1351 Commands
SSD1351_CMD_SETCOLUMN = 0x15
SSD1351_CMD_SETROW = 0x75
SSD1351_CMD_WRITERAM = 0x5C
SSD1351_CMD_READRAM = 0x5D
SSD1351_CMD_SETREMAP = 0xA0
SSD1351_CMD_STARTLINE = 0xA1
SSD1351_CMD_DISPLAYOFFSET = 0xA2
SSD1351_CMD_DISPLAYALLOFF = 0xA4
SSD1351_CMD_DISPLAYALLON = 0xA5
SSD1351_CMD_NORMALDISPLAY = 0xA6
SSD1351_CMD_INVERTDISPLAY = 0xA7
SSD1351_CMD_FUNCTIONSELECT = 0xAB
SSD1351_CMD_DISPLAYOFF = 0xAE
SSD1351_CMD_DISPLAYON = 0xAF
SSD1351_CMD_PRECHARGE = 0xB1
SSD1351_CMD_DISPLAYENHANCE = 0xB2
SSD1351_CMD_CLOCKDIV = 0xB3
SSD1351_CMD_SETVSL = 0xB4
SSD1351_CMD_SETGPIO = 0xB5
SSD1351_CMD_PRECHARGE2 = 0xB6
SSD1351_CMD_SETGRAY = 0xB8
SSD1351_CMD_USELUT = 0xB9
SSD1351_CMD_PRECHARGELEVEL = 0xBB
SSD1351_CMD_VCOMH = 0xBE
SSD1351_CMD_CONTRASTABC = 0xC1
SSD1351_CMD_CONTRASTMASTER = 0xC7
SSD1351_CMD_MUXRATIO = 0xCA
SSD1351_CMD_COMMANDLOCK = 0xFD
SSD1351_CMD_HORIZSCROLL = 0x96
SSD1351_CMD_STOPSCROLL = 0x9E
SSD1351_CMD_STARTSCROLL = 0x9F


class SSD1351_Display(object):
  """ Controller for Adafruit SSD1351 1.5" Color OLED: http://adafru.it/1431 """

  def __init__(self, width, height, rst, dc, spi=None, spi_port=None, spi_device=None, gpio=None):
    """ Initialize the SSD1351

    width: pixel width (128)
    height: pixel height (128)

    rst: reset pin
    dc: dc pin

    spi: SPI device
            spi_port: if SPI object is not passed, then use this spi port
            spi_device: if SPI object is not passed, use this spi device

    gpio: GPIO device. If GPIO is not passed, use the platform gpio

    """

    # Set screen dimensions
    self.width = width
    self.height = height

    # Set up GPIO
    if gpio is not None:
      self._gpio = gpio
    else:
      self._gpio = GPIO.get_platform_gpio()

    # Set up pins
    self._rst = rst
    self._dc = dc
    self._gpio.setup(self._rst, GPIO.OUT)
    self._gpio.setup(self._dc, GPIO.OUT)

    # Set up SPI
    if spi is not None:
      self._spi = spi
    else:
      if spi_port is None or spi_device is None:
        raise ValueError(
            "spi_port and spi_dev must be set if no spi object is passed")
      self._spi = SPI.SpiDev(
          spi_port, spi_device, max_speed_hz=20000000)

    self._spi.set_clock_hz(20000000)

    # Create buffer for images
    self._buffer = [0] * (self.width * self.height)
    self._current_row = 0

  def send_command(self, c):
    """ Send command byte to display """

    self._gpio.set_low(self._dc)
    self._spi.write([c])

  def send_data(self, c):
    """ Send data byte to display """

    self._gpio.set_high(self._dc)
    self._spi.write([c])

  def initialize(self):
    """ Initialize the display """

    # Sending 0x12 unlocks the OLED drive IC and the driver will respond
    # to command and memory access
    # self.send_command(SSD1351_CMD_COMMANDLOCK)  # set command lock
    # self.send_data(0x12)

    # Not sure of the purpose of sending 0xB1
    # This has to do with the start row offset
    self.send_command(SSD1351_CMD_COMMANDLOCK)  # set command lock
    self.send_data(0xB1)

    # Sleep mode on (that is, display is off)
    self.send_command(SSD1351_CMD_DISPLAYOFF)   # 0xAE

    # Set front clock divider and oscillator frequency
    self.send_command(SSD1351_CMD_CLOCKDIV)     # 0xB3
    # 7:4 = Oscillator Frequency, 3:0 = CLK Div Ratio (A[3:0]+1 = 1..16)
    self.send_command(0xD1)

    # Set the multiplex ratio.
    self.send_command(SSD1351_CMD_MUXRATIO)
    self.send_data(127)

    # Set the remapping
    self.send_command(SSD1351_CMD_SETREMAP)
    # 0x74 = 1110100
    # A[0] = Address increment mode. 0 = horizontal address increment mode; 1 = vertical address increment mode
    # A[1] = Column address remap. 0 = RAM 0~127 maps to Col0~127; 1 = RAM 0~127 maps to Col127~0
    # A[2] = Color remap. 0 = (reset) color sequence A -> B -> C; 1 = color sequence C -> B -> A
    # A[4] = COM scan direction remap. 0 = scan from up to down, 1 = scan from bottom to up
    # A[5] = Odd even splits of COM pins. 0 = (reset) odd/even; 1 = ?
    # A[7:6] = Display color mode. Select either 262l, 65;, 265 color mode
    self.send_data(0x74)

    # Set display start line. We like to start at the top (zero)
    self.send_command(SSD1351_CMD_STARTLINE)
    self.send_data(0)  # This may be 96 for the 128x96 screen?

    # Set the display offset
    self.send_command(SSD1351_CMD_DISPLAYOFFSET)
    self.send_data(0x00)

    # Set the GPIO options
    self.send_command(SSD1351_CMD_SETGPIO)
    self.send_data(0x00)

    # Enable or disable the VDD register.
    self.send_command(SSD1351_CMD_FUNCTIONSELECT)
    self.send_data(0x01)

    # Set the phase length of the OLED
    self.send_command(SSD1351_CMD_PRECHARGE)
    self.send_command(0x32)
    # self.send_command(0x01)

    # Set voltage
    self.send_command(SSD1351_CMD_VCOMH)
    self.send_command(0x05)  # This is the reset value

    # Set the display on
    self.send_command(SSD1351_CMD_NORMALDISPLAY)

    # Set the contrast current for each color (0x00 to 0xFF)
    self.send_command(SSD1351_CMD_CONTRASTABC)
    self.send_data(0xC8)
    self.send_data(0x80)
    self.send_data(0xC8)

    # Master contrast current control. The smaller the master current, the dimmer the OLED.
    # 16 steps: 0000b to 1111b (default)
    self.send_command(SSD1351_CMD_CONTRASTMASTER)
    self.send_data(0x0F)  # Max

    # Set the low voltage
    self.send_command(SSD1351_CMD_SETVSL)
    self.send_data(0xA0)
    self.send_data(0xB5)
    self.send_data(0x55)

    # Set the second precharge period
    self.send_command(SSD1351_CMD_PRECHARGE2)
    self.send_data(0x01)  # Minimum: 1 DCLKS

    # Leave sleep mode
    self.send_command(SSD1351_CMD_DISPLAYON)

  def reset(self):
    """ Reset the display. When reset is pulled low, the chip is
    initialized with the following state:

    1. Display is OFF
    2. 128 MUX display mode
    3. Normal segment address mapping
    4. Display start line is set to RAM address 0
    5. Column address counter is set to 0
    6. Normal scan direction of the COM outputs
    7. Some commands locked
    """

    # Set reset high for a millisecond
    self._gpio.set_high(self._rst)
    time.sleep(0.001)

    # Set reset low for 10 ms
    self._gpio.set_low(self._rst)
    time.sleep(0.010)

    # Set reset high again
    self._gpio.set_high(self._rst)

  def start_display(self):
    """ Initialize the display """

    self.reset()
    self.clear_buffer()
    self.write_buffer()
    self.initialize()

  def clear_buffer(self):
    """ Clear the display buffer """

    self._buffer = [0] * (self.width * self.height)

  def write_buffer(self):
    """ Write the complete buffer to the display """

    self.send_command(SSD1351_CMD_SETCOLUMN)
    self.send_data(0)
    self.send_data(self.width - 1)  # Column end address

    self.send_command(SSD1351_CMD_SETROW)
    self.send_data(0)
    self.send_data(self.height - 1)  # Row end

    # Write buffer data
    self._gpio.set_high(self._dc)
    self.send_command(SSD1351_CMD_WRITERAM)

    buf = []
    for i in xrange(len(self._buffer)):
      buf.append(self._buffer[i] >> 8)
      buf.append(self._buffer[i])

    # Write the array directly to output
    self._gpio.set_high(self._dc)
    self._spi.write(buf)

  def write_line(self, line):
    """ Add a new line to the bottom and scroll the current image up.
    line should be length self.width
    """
    assert len(line) == self.width

    # Increment the scrolling row
    self._current_row = self._current_row + 1
    if self._current_row >= self.height:
      self._current_row = 0

    # Set scrolling to the current place
    self.send_command(SSD1351_CMD_STARTLINE)
    self.send_data(self._current_row)

    # Set up for writing this one row
    self.send_command(SSD1351_CMD_SETCOLUMN)
    self.send_data(0)
    self.send_data(self.width - 1)  # Column end address

    self.send_command(SSD1351_CMD_SETROW)
    self.send_data(self._current_row - 1)
    self.send_data(self._current_row - 1)

    # Write buffer data
    self.send_command(SSD1351_CMD_WRITERAM)
    buf = []
    for i in xrange(len(line)):
      buf.append(line[i] >> 8)
      buf.append(line[i])

    # Write the array directly to output
    self._gpio.set_high(self._dc)
    self._spi.write(buf)

  def load_image(self, image):
    """ Set buffer to PIL image """

    # Make sure it's an RGB with correct width and height
    image = image.resize((self.width, self.height), Image.ANTIALIAS)
    image = image.convert("RGB")

    # Extract the pixels
    pix = image.load()

    # Add each pixel to the buffer
    i = 0
    w, h = image.size
    for row in xrange(0, h):
      for col in xrange(0, w):
        r, g, b = pix[col, row]
        color = color565(r, g, b)
        self._buffer[i] = color
        i += 1


def color565(red, green=None, blue=None):
  """ Define color in 16-bit RGB565. Red and blue
  have five bits each and green has 6 (since the
  eye is more sensitive to green).

  Bit Format: RRRR RGGG GGGB BBBB

  Usage:
  color565(red=[0,255], green=[0,255], blue=[0,255)
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
