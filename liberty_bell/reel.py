import random

class Reel(object):
    """ A slot machine reel  """

    def __init__(self, name, stops, randomizer=random):
        """ Initialize the reel """

        self.name = name
        self.stops = stops

        self.randomizer = randomizer

    def __str__(self):
        """ Print details """

        return str(self.name)

    def spin(self):
        """ Spin the reel and return a random result """

        return self.randomizer.choice(self.stops)
