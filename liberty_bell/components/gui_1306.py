import os
import textwrap
import Tkinter as tk

import PIL.Image as Image
import PIL.ImageChops as ImageChops
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
import PIL.ImageTk as ImageTk

dir = os.path.dirname(__file__)

FONT_PATH = os.path.join(dir, '../fonts/Moder DOS 437.ttf')
FONT_SIZE = 16


class GUI_1306(tk.Label, object):
  """ This behaves like the SSD1306 Display Adapter """

  def __init__(self, *args, **kwargs):

    self.width = 128
    self.height = 64

    self._image = Image.new("RGB", (self.width, self.height), color="#000000")

    tk.Label.__init__(self, *args, **kwargs)

    self.update_image()

  def blank(self):
    self._image = Image.new("RGB", (self.width, self.height), color="#000000")

  def clear(self):
    self.blank()
    self.update_image()

  def update_image(self):
    """ Write image to the screen """

    tkimage = ImageTk.PhotoImage(self._image)

    self.image = tkimage
    self.configure(image=tkimage)
    self.update()

  def display(self):
    self.update_image()

  def text(self, text, x=0, y=10, font_size=FONT_SIZE, color=(255, 255, 255)):
    """ Draw text on the screen """

    y_text = y

    font = ImageFont.truetype(FONT_PATH, font_size)
    lines = textwrap.wrap(text, width=14)

    draw = ImageDraw.Draw(self._image)

    for line in lines:
      width, height = font.getsize(line)
      draw.text((x, y_text), line, font=font, fill=color)
      y_text += height

    self.update_image()

  def menu_text(self, text, up=False, down=False, child=False):
    """ Trying to draw better..."""

    y = 0

    headline = "MENU"

    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    headline_size_x, headline_size_y = font.getsize(headline)

    draw = ImageDraw.Draw(self._image)

    y += headline_size_y

    # Draw a white background for the headline
    draw.rectangle((0, 0, self.width, headline_size_y), fill=(255, 255, 255))
    draw.text((0, 0), headline, font=font, fill=(0, 0, 0))

    # Draw the text
    lines = textwrap.wrap(text, width=14)
    for line in lines:
      width, height = font.getsize(line)
      draw.text((0, y), line, font=font, fill=(255, 255, 255))
      y += height
