import copy
import random

from liberty_bell.slot_machines.components.reel_image import ReelImage


class Reel(object):
    """ A slot machine reel  """

    def __init__(self, index, stops, randomizer=random):
        """ Initialize the reel """

        self.index = index
        self.name = "Reel %i" % (index + 1)
        self.stops = copy.deepcopy(stops)

        self.winning_stop = None
        self.winning_symbol = None

        self.randomizer = randomizer

    def __str__(self):
        return str(self.name)

    def get_image(self):
        """ Return the image of the reel """

        return ReelImage(self.stops)

    def spin(self, min_spins=None):
        """ Spin the reel and return a random result """

        self.winning_stop = self.randomizer.choice(range(len(self.stops)))

        # Randomly choose a winning symbol
        self.winning_symbol = self.stops[self.winning_stop]

        print "Reel %s Winning symbol %s" % (self.name, self.winning_symbol)
