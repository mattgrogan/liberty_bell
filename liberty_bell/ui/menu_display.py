""" Class for controlling the menu data display """
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont


dir = os.path.dirname(__file__)

FONT_PATH = os.path.join(dir, '../fonts/Moder DOS 437.ttf')
FONT_SIZE = 16

DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64
TEXT_WIDTH = 14


class Menu_Display(object):

    def __init__(self, display_driver):

        self._display_driver = display_driver
        self.width = DISPLAY_WIDTH
        self.height = DISPLAY_HEIGHT
        self.size = (self.width, self.height)
        self.font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

        self._image = None

        self.clear()

    def clear(self):

        self._image = Image.new("1", self.size, color="#000000")
        self._draw = ImageDraw.Draw(self._image)

    def flush(self):
        """ Write to the hardware """

        self._display_driver.display(self._image)

    def add_line(self, line, loc=(0, 0), inverse=False):
        """ Write a single line of text. Returns the width and height
        of the line """

        # Obtain drawing object
        #draw = ImageDraw.Draw(self._image)
        draw = self._draw

        x, y = loc
        width, height = self.font.getsize(line)

        color = "#FFFFFF"
        background = "#000000"

        if inverse:
            color, background = background, color

        # Draw the background for the entire display width
        draw.rectangle([loc, (x + self.width, y + height)], fill=background)
        draw.text(loc, line, font=self.font, fill=color)

        return (width, height)

    def add_line_nbr(self, line, line_num, inverse=False):
        """ Add the first line """
        width, height = self.font.getsize(line)
        y = height * line_num
        self.add_line(line, (0, y), inverse)

    def add_wrapped_text(self, text, loc=(0, 0)):

        x, y = loc

        # Wrap the text
        lines = textwrap.wrap(text, width=TEXT_WIDTH)

        for line in lines:
            print "Printing '%s' at (%i, %i)" % (line, x, y)
            width, height = self.add_line(line, (x, y))
            y += height

    def add_menu_text(self, text, headline="MENU"):

        width, height = self.add_line(headline, inverse=True)
        self.add_wrapped_text(text, loc=(0, height))
