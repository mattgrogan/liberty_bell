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

class Slot_Machine(object):
    """ A superclass for slot machines """

    def __init__(self, randomizer=random):
        """ Initialize the machine """

        self.name = "Slot Machine"
        self.credits = None
        self.bet = None
        self.reels = []
        self.randomizer = randomizer

        # Set up events
        events = ["CREDITS_CHANGED", "PAYOUT", "PLACE_BET", "BET_CHANGED"]

        self.events = {event: dict() for event in events}

    def register(self, event, who, callback=None):
        """ Register for updates """

        if callback is None:
            callback = getattr(who, 'update')

        self.events[event][who] = callback

    def notify(self, event, message=None):
        """ Notify the subscribers for a particular event """

        for subscriber, callback in self.events[event].iteritems():
            callback(message)

    def payout(self, amount):
        """ Add to the credits """

        self.credits += amount

        self.notify("PAYOUT", amount)
        self.notify("CREDITS_CHANGED", self.credits)

    def set_credits(self, credits):
        """ Set the credits to a specific amount """

        self.credits = credits
        self.notify("CREDITS_CHANGED", self.credits)

    def set_bet(self, bet):
        """ Set the bet to an arbitrary amount """

        self.bet = bet
        self.notify("BET_CHANGED", bet)

    def place_bet(self):
        """ Place the bet and remove the amount from the credits """

        # You can't bet more than your credits!
        assert self.bet <= self.credits
        self.credits -= self.bet

        self.notify("PLACE_BET", self.bet)
        self.notify("CREDITS_CHANGED", self.credits)

        return self.bet

    def increment_bet(self):
        """ Increment the bet by one """

        if (self.bet + 1) > self.credits:
            raise ValueError("Not enough credits")

        if self.bet < MAX_BET:
            self.bet += 1
            self.notify("BET_CHANGED", self.bet)

    def decrement_bet(self):
        """ Decrement the bet by one """

        if self.bet > 1:
            self.bet -= 1
            self.notify("BET_CHANGED", self.bet)

    def spin(self):
        """ Spin all three reels """

        # Take the bet
        bet = self.place_bet()

        reels = []

        for reel in self.reels:
            reels.append(reel.spin())

        winner_paid = self.payout_table.calculate_payout(reels) * bet

        # Add the winnings, if any
        self.payout(winner_paid)

        spin_result = Spin_Result(reels, winner_paid)

        return spin_result

class Liberty_Bell_Machine(Slot_Machine):
    """ A slot machine based on the original Liberty Bell machine """

    def __init__(self, *args, **kwargs):
        """ Initialize the Liberty Bell slot Machine """

        super(Liberty_Bell_Machine, self).__init__(*args, **kwargs)

        self.name = "Liberty Bell"
        self.reels = []

        # Add the three reels
        for i in range(3):
            reel_name = "Reel %i" % i
            reel = Liberty_Bell_Reel(name=reel_name)
            reel.set_randomizer(self.randomizer)
            self.reels.append(reel)

        # Add the payout table
        self.payout_table = Liberty_Bell_Payout_Table()
