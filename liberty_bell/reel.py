import random
from symbols import Liberty_Bell_Symbols
from spin_result import Spin_Result

symbols = Liberty_Bell_Symbols()

class Liberty_Bell_Reel(object):
    """ A slot machine reel based on the original Liberty Bell machine """

    def __init__(self, name, stops):
        """ Initialize the reel """

        self.name = name
        self.stops = [symbols.LIBERTY_BELL, symbols.HEART, symbols.DIAMOND,
                      symbols.SPADE, symbols.SPADE, symbols.SPADE,
                      symbols.HORSESHOE, symbols.HORSESHOE, symbols.HORSESHOE,
                      symbols.STAR]

        self.randomizer = random

    def __str__(self):
        """ Print details """

        return str(self.name)

    def set_randomizer(self, randomizer):
        """ Set a deterministic randomizer for testing """

        self.randomizer = randomizer

    def spin(self):
        """ Spin the reel and return a random result """

        return self.randomizer.choice(self.stops)
