import random
from symbols import Liberty_Bell_Symbols
from spin_result import Spin_Result

symbols = Liberty_Bell_Symbols()


class RandomMock(object):
    """ Mock random.choice for testing """

    def __init__(self, sequence=None):
        """ Initialize at place zero """

        self.index = 0
        self.sequence = sequence

    def choice(self, stops):
        """ Return the item deterministicaly """

        # If we weren't passed a sequence of values, then just use
        # the stops.
        if self.sequence is None:
            self.sequence = range(len(stops))

        # Reset index if it's out of range
        if self.index >= len(self.sequence):
            self.index = 0

        # Find the result in the current item
        stop_index = self.sequence[self.index]
        result = stops[stop_index]

        self.index = self.index + 1
        return result


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


class Simple_Three_Reel_Machine(object):
    """ A slot machine with three reels and identical stops on
    each reel """

    def __init__(self, name, stops, randomizer=random):
        """ Initialize the machine """

        self.name = name
        self.reels = []

        for i in range(3):
            reel_name = "Reel %i" % i
            reel = Liberty_Bell_Reel(name=reel_name, stops=stops)
            reel.set_randomizer(randomizer)
            self.reels.append(reel)

    def spin(self):
        """ Spin all three reels """

        result = Spin_Result()

        for reel in self.reels:
            result.add_reel_symbol(reel.spin())

        result.calculate_payout()

        return result
