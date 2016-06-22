import random
from reel import Reel
from payout import Payout_Table, Payline
from spin_result import Spin_Result
from events import Events
from symbols import Liberty_Bell_Symbols

symbols = Liberty_Bell_Symbols()

MAX_BET = 10


class Slot_Machine(object):
    """ A superclass for slot machines """

    def __init__(self, randomizer=random):
        """ Initialize the machine """

        self.name = "Slot Machine"
        self.credits = None
        self.bet = None
        self.reels = []
        self.randomizer = randomizer
        self.payout_table = Payout_Table()

        # Set up events
        events = [Events.CREDITS_CHANGED, Events.PAYOUT,
                  Events.PLACE_BET, Events.BET_CHANGED]

        self.events = {event: dict() for event in events}

    def add_reel(self, name, stops):
        """ Add a reel to the machine """

        reel = Reel(name, stops)
        reel.set_randomizer(self.randomizer)
        self.reels.append(reel)

    def initialize(self, credits=None, bet=None):
        """ Initialize credit and/or bet values """

        if credits is not None:
            self.credits = credits
            self.notify(Events.CREDITS_CHANGED, self.credits)

        if bet is not None:
            self.bet = bet
            self.notify(Events.BET_CHANGED, bet)

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

        self.notify(Events.PAYOUT, amount)
        self.notify(Events.CREDITS_CHANGED, self.credits)

    def place_bet(self):
        """ Place the bet and remove the amount from the credits """

        # You can't bet more than your credits!
        assert self.bet <= self.credits
        self.credits -= self.bet

        self.notify(Events.PLACE_BET, self.bet)
        self.notify(Events.CREDITS_CHANGED, self.credits)

        return self.bet

    def increment_bet(self, message=None):
        """ Increment the bet by one """

        if (self.bet + 1) > self.credits:
            raise ValueError("Not enough credits")

        if self.bet < MAX_BET:
            self.bet += 1
            self.notify(Events.BET_CHANGED, self.bet)

    def decrement_bet(self, message=None):
        """ Decrement the bet by one """

        if self.bet > 1:
            self.bet -= 1
            self.notify(Events.BET_CHANGED, self.bet)

    def spin(self):
        """ Spin the reels """

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

        stops = [symbols.LIBERTY_BELL, symbols.HEART, symbols.DIAMOND,
                 symbols.SPADE, symbols.SPADE, symbols.SPADE,
                 symbols.HORSESHOE, symbols.HORSESHOE, symbols.HORSESHOE,
                 symbols.STAR]

        # Add the three reels
        for i in range(3):
            self.add_reel(name="Reel %i" % (i + 1), stops=stops)

        # Add the paylines to the payout table
        self.payout_table.append(Payline({symbols.LIBERTY_BELL: 3}, 20))
        self.payout_table.append(Payline({symbols.HEART: 3}, 16))
        self.payout_table.append(Payline({symbols.DIAMOND: 3}, 12))
        self.payout_table.append(Payline({symbols.SPADE: 3}, 8))
        self.payout_table.append(
            Payline({symbols.HORSESHOE: 2, symbols.STAR: 1}, 4))
        self.payout_table.append(Payline({symbols.HORSESHOE: 2}, 2))
