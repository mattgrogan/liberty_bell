from PIL import Image

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

    def __str__(self):
        """ Convert to string """

        return self.name

    def __eq__(self, other):
        """ Check for equality """

        return self.name == other.name
