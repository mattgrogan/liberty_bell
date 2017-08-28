from PIL import Image


class ReelImage(object):
    """ Encapsulate a scrollable image for all the reel symbols """

    def __init__(self, stops):
        """ Pass reel to get the images """

        self.stops = stops    # The slot machine reel holds an image for each symbol
        self.image = None

        self.w = 0     # The width of the entire reel image
        self.h = 0     # The height of the entire reel image

        self.calculate_height()
        self.stitch_image()

        #self.image.show()

    def calculate_height(self):
        """ Loop through the stops to determine the overall image dimensions """

        for stop in self.stops:
            # Extract the dimensions from the reel stop images
            img = stop.image.image
            width, height = img.size

            # The entire width will be the maximum of any of the images
            self.w = max(self.w, width)

            # Increment the height for each image
            self.h += height

    def stitch_image(self):
        """ Stitch the image into one long image """

        # Stitch the image together
        self.image = Image.new("RGB", (self.w, self.h))

        x = 0
        y = 0

        for stop in self.stops:
            self.image.paste(stop.image.image, (x, y))
            width, height = stop.image.image.size
            y += height
