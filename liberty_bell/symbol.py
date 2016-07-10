from PIL import Image, ImageOps

SSD1351_WIDTH = 128
SSD1351_HEIGHT = 128

class Symbol(object):
    """ Superclass for symbols on the slot machine """

    def __init__(self, name, img_path=None):
        """ Initialize the symbol """

        self.name = name
        self.img_path = img_path
        self.image = None
        self.width = SSD1351_WIDTH
        self.height = SSD1351_HEIGHT

        if self.img_path is not None:
            # Load the image
            self.image = Image.open(self.img_path)

            #TODO: Move this out of here! Symbol should know nothing about screen size.
            # Resize for the screen
            # TODO: make sure the width and height and border tuples are in the correct order
            # it might work only because we're dealing with squares
            if self.image.size != (SSD1351_WIDTH, SSD1351_HEIGHT):
                width_diff = SSD1351_WIDTH - self.image.size[0]
                height_diff = SSD1351_HEIGHT - self.image.size[1]
                border_size = (width_diff / 2, width_diff / 2, height_diff / 2, height_diff / 2)
                self.image = ImageOps.expand(self.image, border = border_size)

        # Make sure it's RGB
        self.image = self.image.convert("RGB")

        # Stash the pixels
        pix = self.image.load()
        w, h = self.image.size
        self.pix565 = [[0 for x in range(w)] for y in range(h)]

        for y in range(h):
            for x in range(w):
                r, g, b = pix[y, x]
                self.pix565[x][y] = color565(r, g, b) #This is rotating the image


    def __str__(self):
        """ Convert to string """

        return self.name

    def __eq__(self, other):
        """ Check for equality """

        return self.name == other.name

    def get_row(self, row_number):
        """ Get a single row from the image """

        return self.pix565[:][row_number]

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
