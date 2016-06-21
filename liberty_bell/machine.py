import random
from reel import Liberty_Bell_Reel
from payout import Liberty_Bell_Payout_Table
from spin_result import Spin_Result

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

class Liberty_Bell_Machine(object):
    """ A slot machine based on the original Liberty Bell machine """

    def __init__(self, name, randomizer=random):
        """ Initialize the machine """

        self.name = name
        self.reels = []

        # Add the three reels
        for i in range(3):
            reel_name = "Reel %i" % i
            reel = Liberty_Bell_Reel(name=reel_name)
            reel.set_randomizer(randomizer)
            self.reels.append(reel)

        # Add the payout table
        self.payout_table = Liberty_Bell_Payout_Table()

    def spin(self):
        """ Spin all three reels """

        reels = []

        for reel in self.reels:
            reels.append(reel.spin())

        winner_paid = self.payout_table.calculate_payout(reels)

        spin_result = Spin_Result(reels, winner_paid)

        return spin_result
