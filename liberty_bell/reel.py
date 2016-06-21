import random


class RandomMock(object):
    """ Mock random.choice for testing """

    def __init__(self):
        """ Initialize at place zero """

        self.index = 0

    def choice(self, stops):
        """ Return the item deterministicaly """

        # Reset index if it's out of range
        if self.index >= len(stops):
            self.index = 0

        # Return the current item
        result = stops[self.index]
        self.index = self.index + 1
        return result

class Reel(object):
    """ A slot machine reel """

    def __init__(self, name, stops):
        """ Initialize the reel """

        self.name = name
        self.stops = stops

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
