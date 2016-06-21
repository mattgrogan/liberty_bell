import random
from reel import Liberty_Bell_Reel
from payout import Liberty_Bell_Payout_Table
from spin_result import Spin_Result

MAX_BET = 10

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

class Machine_Bank(object):
    """ The bank holds the player's credits """

    def __init__(self):
        """ Initialize with 100 creedits """

        self.credits = 100
        self.bet = 1

    def payout(self, amount):
        """ Add to the credits """

        self.credits += amount

    def place_bet(self):
        """ Place the bet and remove the amount from the credits """

        # You can't bet more than your credits!
        assert self.bet <= self.credits
        self.credits -= self.bet

        return self.bet

    def increment_bet(self):
        """ Increment the bet by one """

        if (self.bet + 1) > self.credits:
            raise ValueError("Not enough credits")

        if self.bet < MAX_BET:
            self.bet += 1

    def decrement_bet(self):
        """ Decrement the bet by one """

        if self.bet > 1:
            self.bet -= 1

class Liberty_Bell_Machine(object):
    """ A slot machine based on the original Liberty Bell machine """

    def __init__(self, name, randomizer=random):
        """ Initialize the machine """

        self.name = name
        self.reels = []
        self.bank = Machine_Bank()

        # Add the three reels
        for i in range(3):
            reel_name = "Reel %i" % i
            reel = Liberty_Bell_Reel(name=reel_name)
            reel.set_randomizer(randomizer)
            self.reels.append(reel)

        # Add the payout table
        self.payout_table = Liberty_Bell_Payout_Table()

    def increment_bet(self):
        """ Tell the bank to increment the bet by one """

        self.bank.increment_bet()

    def decrement_bet(self):
        """ Tell the bank to decrement the bet by one """

        self.bank.decrement_bet()

    def spin(self):
        """ Spin all three reels """

        # Take the bet
        bet = self.bank.place_bet()

        reels = []

        for reel in self.reels:
            reels.append(reel.spin())

        winner_paid = self.payout_table.calculate_payout(reels) * bet

        # Add the winnings, if any
        self.bank.payout(winner_paid)

        spin_result = Spin_Result(reels, winner_paid)

        return spin_result
