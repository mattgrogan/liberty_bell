import random
import time

from liberty_bell.config import Config
from liberty_bell.slot_machines.components.pay_table import Pay_Table
from liberty_bell.slot_machines.components.payline import Payline
from liberty_bell.slot_machines.components.reel import Reel
from liberty_bell.slot_machines.components.spin_result import Spin_Result


class Slot_Machine(object):
    """ A superclass for slot machines """

    def __init__(self, randomizer=random):
        """ Initialize the machine """

        config = Config()

        self.name = "Slot Machine"
        self._credits = config.default_credits
        self.prev_credits = 0
        self.winner_paid = 0
        self.bet = config.default_bet
        self.spin_result = None

        self.denomination = 0.01

        self.max_bet = config.max_bet
        self.payout_delay_secs = config.payout_delay_secs

        self.symbols = []
        self.reels = []
        self.randomizer = randomizer
        self.payout_table = Pay_Table()

    @property
    def credits(self):
        return self._credits

    @credits.setter
    def credits(self, value):
        if value != self._credits:
            self.prev_credits = self._credits
            self._credits = value

    @property
    def is_spinning(self):
        return self.spin_result is not None

    def add_reel(self, stops):
        """ Add a reel to the machine """

        reel = Reel(index=len(self.reels), stops=stops,
                    randomizer=self.randomizer)
        self.reels.append(reel)

    def place_bet(self):
        """ Place the bet and remove the amount from the credits """

        # You can't bet more than your credits!
        assert self.bet is not None
        assert self.bet > 0
        assert self.credits is not None
        assert self.bet <= self.credits
        self.credits -= self.bet

        self.winner_paid = 0

        return self.bet

    @property
    def can_increase_bet(self):
        """ Do we have enough credits to increase the bet """

        below_max_bet = self.bet < self.max_bet
        bet_is_below_credits = self.bet < self.credits

        return below_max_bet and bet_is_below_credits and not self.is_spinning

    @property
    def can_decrease_bet(self):
        """ Do we have at least one credit? """

        return self.bet > 1 and not self.is_spinning

    @property
    def can_spin(self):
        """ Return true if there's enough credits to spin """

        return self.bet <= self.credits and not self.is_spinning

    def increment_bet(self, message=None):
        """ Increment the bet by one """

        attempted_bet = self.bet + 1

        if attempted_bet <= self.credits and attempted_bet <= self.max_bet:
            self.bet = attempted_bet

    def decrement_bet(self, message=None):
        """ Decrement the bet by one """

        if self.bet > 1:
            self.bet -= 1

    def spin(self):
        """ Spin the reels """

        assert len(self.reels) > 0

        # Take the bet
        bet = self.place_bet()

        reels = []
        for reel in self.reels:
            reel.spin()
            reels.append(reel.winning_symbol)

        self.spin_result = Spin_Result(reels, winner_paid=None)

    def eval_spin(self):
        """ Evaluate the spin """

        self.winner_paid = self.payout_table.calculate_payout(
            self.spin_result.reels) * self.bet

        self.credits += self.winner_paid

        self.spin_result = None

        return self.winner_paid > 0
