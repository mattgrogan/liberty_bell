from PIL import Image, ImageOps


class Symbol_Image(object):

    def __init__(self, path, width, height):

        self.path = path
        self.width = width
        self.height = height

        self.image = None

        self._current_row = 0  # for the iterations

        self.load_image()

    def load_image(self):
        """ Load the image from the file """

        try:
            self.image = Image.open(self.path)
        except:
            self.image = Image.new("RGB", (self.width, self.height), "#FF0000")

        # Resize the image if necessary
        if self.image.size != (self.width, self.height):
            wb = (self.width - self.image.size[0]) / 2
            hb = (self.height - self.image.size[1]) / 2
            border_size = (wb, wb, hb, hb)
            self.image = ImageOps.expand(self.image, border=border_size)

        self.image = self.image.convert("RGB")

    def reset(self):
        self._current_row = 0

    def next_line(self):
        """ Extract a single row from the image """

        if self._current_row >= self.height:
            raise StopIteration()

        row_data = []
        pix = self.image.load()

        for i in range(self.width):
            row_data.append(pix[i, self._current_row])

        self._current_row += 1

        return row_data
