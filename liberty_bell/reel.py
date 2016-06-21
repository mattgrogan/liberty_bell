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

class Simple_Three_Reel_Machine(object):
    """ A slot machine with three reels and identical stops on
    each reel """

    def __init__(self, name, stops, randomizer = random):
        """ Initialize the machine """

        self.name = name
        self.reels = []

        for i in range(3):
            reel_name = "Reel %i" % i
            reel = Reel(name = reel_name, stops = stops)
            reel.set_randomizer(randomizer)
            self.reels.append(reel)

    def spin(self):
        """ Spin all three reels """

        result = []

        for reel in self.reels:
            result.append(reel.spin())

        return result
