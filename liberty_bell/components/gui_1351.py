import Tkinter as tk

import PIL.Image as Image
import PIL.ImageChops as ImageChops
import PIL.ImageTk as ImageTk


class GUI_1351(tk.Label, object):
    """ This behaves like the SSD1351 Display Adapter """

    def __init__(self, *args, **kwargs):

        self.width = 128
        self.height = 128

        self._image = Image.new(
            "RGB", (self.width, self.height), color="#000000")

        tk.Label.__init__(self, *args, **kwargs)

        self.update_image()

    def clear(self):
        self._image = Image.new(
            "RGB", (self.width, self.height), color="#000000")
        self.update_image()

    def update_image(self):
        """ Write image to the screen """

        tkimage = ImageTk.PhotoImage(self._image)

        self.image = tkimage
        self.configure(image=tkimage)
        self.update()

    def write_line(self, line):

        # Offset by -1 to scroll upwards
        self._image = ImageChops.offset(self._image, 0, -1)
        pix = self._image.load()

        for i, pixel in enumerate(line):
            pix[i, self.height - 1] = pixel

        self.update_image()
