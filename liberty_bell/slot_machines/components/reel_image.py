from PIL import Image


class ReelImage(object):
    """ Encapsulate a scrollable image for all the reel symbols """

    def __init__(self, stops):
        """ Pass reel to get the images """

        self.stops = stops    # The slot machine reel holds an image for each symbol

        self.current_row = 0

        self.reel_width = 0      # The width of the entire reel image
        self.reel_height = 0     # The height of the entire reel image

        # Determine the reel height
        for stop in self.stops:
            # Extract the dimensions from the reel stop images
            img = stop.image.image
            width, height = img.size

            # The entire width will be the maximum of any of the images
            self.reel_width = max(self.reel_width, width)

            # Increment the height for each image
            self.reel_height += height

        # Stitch the image together
        self.image = Image.new("RGB", (self.reel_width, self.reel_height))

        x = 0
        y = 0

        for stop in self.stops:
            self.image.paste(stop.image.image, (x, y))
            width, height = stop.image.image.size
            y += height

    def next_line(self):
        """ Extract a single row from the image """

        if self.current_row >= self.reel_height:
            raise StopIteration()

        self.pix = self.image.load()

        row_data = []

        for i in range(self.reel_width):
            row_data.append(self.pix[i,self.current_row])

        self.current_row += 1

        return row_data
