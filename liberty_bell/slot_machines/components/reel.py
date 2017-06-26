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

        self.winning_symbol = None

        self.current_stop = 0
        self.current_spin = 0

        self.min_spins = index + 1

        self.randomizer = randomizer

    def __str__(self):
        return str(self.name)

    @property
    def current_symbol(self):
        """ Return the current symbol to be shown in the ui """

        return self.stops[self.current_stop]

    def advance(self):
        """ Advance the reel to the next stop and return the symbol """

        self.current_stop = self.current_stop + 1

        if self.current_stop >= len(self.stops):
            self.current_stop = 0  # go around
            self.current_spin = self.current_spin + 1

        self.current_symbol.image.reset()

    def spin(self, min_spins=None):
        """ Spin the reel and return a random result """

        # TODO: This can be changed to "skip symbol" logic instead
        # for example, skip 3 horseshoes before landing on the winning symbol

        if min_spins is None:
            min_spins = self.index + 1

        # Randomly choose a winning symbol
        self.winning_symbol = self.randomizer.choice(self.stops)

        print "Reel %s Winning symbol %s" % (self.name, self.winning_symbol)

        # Calculate the minimum number of stops
        min_stops = min_spins * len(self.stops)

        spin_stops = []

        # Get each stop for the minimum number of spins
        for i in range(min_stops):
            self.advance()
            spin_stops.append(self.current_symbol)

        # Now iterate until we find the winning symbol
        while self.current_symbol != self.winning_symbol:
            self.advance()
            spin_stops.append(self.current_symbol)

        self.spin_image = ReelImage(spin_stops)

    def next_line(self):
        """ Get the next line from the symbol """

        return self.spin_image.next_line()
