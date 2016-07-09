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

        if self.img_path is not None:
            # Load the image
            self.image = Image.open(self.img_path)

            #TODO: Move this out of here!
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

    def __str__(self):
        """ Convert to string """

        return self.name

    def __eq__(self, other):
        """ Check for equality """

        return self.name == other.name
