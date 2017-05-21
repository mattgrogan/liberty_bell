import math
import numpy as np

from PIL import Image, ImageOps


class Symbol_Image_W(object):
  """ Modification of Symbol_Image that forces a white background """

  def __init__(self, path, width, height):

    self.path = path
    self.width = width
    self.height = height

    self.image = None

    self._current_row = 0  # for the iterations

    self.load_image()

  def load_image(self):
    """ Load the image from the file """

    #try:
    png = Image.open(self.path)
    #except:
    #  png = Image.new("RGB", (self.width, self.height), "#FF0000")

    if png.mode == "RGBA":
      # Fill the alpha channel with white
      png.load()  # Required for png.split()
      background = Image.new("RGB", png.size, (255, 255, 255))
      background.paste(png, mask=png.split()[3])
      self.image = background
    else:
      self.image = png

    w, h = self.image.size

    if w < self.width or h < self.height:
      # The image is smaller than the screen. How much smaller?
      w_delta = self.width - w
      h_delta = self.height - h

      # Find the size of the cardinal directions
      e = int(math.floor(w_delta / 2))
      w = int(w_delta - e)
      n = int(math.floor(h_delta / 2))
      s = int(h_delta - n)

      border_size = (e, n, w, s)

      self.image = ImageOps.expand(
          self.image, border=border_size, fill="#FFFFFF")
    elif w > self.width or h > self.width:
      # Image is bigger than the screen. Resize it.
      self.image.resize((self.width, self.height))

    # Remove any alpha channel
    self.image = self.image.convert("RGB")

    self.pix = None

  def reset(self):
    self._current_row = 0

  def stash_pixels(self, pixel_converter=None):
    """ Prepare pixes for screen """

    # TODO: Handle pixel conversions for the gui

    pixels = self.image.load()

    w, h = self.image.size
    self.pix = [[0 for x in range(w)] for y in range(h)]

    for y in range(h):
      for x in range(w):
        r, g, b = pixels[x, y]
        self.pix[x][y] = pixel_converter.convert(r, g, b)

  def next_line(self):
    """ Extract a single row from the image """

    if self.pix is None:
      self.stash_pixels(Color565())

    if self._current_row >= self.height:
      raise StopIteration()

    row_data = []

    for i in range(self.width):
      row_data.append(self.pix[i][self._current_row])

    self._current_row += 1

    return row_data

class Color565(object):
  """ Convert a color to RGB565 """

  def convert(self, red, green, blue):
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
