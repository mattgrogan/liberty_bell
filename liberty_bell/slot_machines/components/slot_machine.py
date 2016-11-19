import random
import time

from config import Config
from pay_table import Pay_Table
from payline import Payline
from reel import Reel
from spin_result import Spin_Result


class Slot_Machine(object):
  """ A superclass for slot machines """

  def __init__(self, randomizer=random):
    """ Initialize the machine """

    config = Config()

    self.name = "Slot Machine"
    self.credits = config.default_credits
    self.winner_paid = 0
    self.bet = config.default_bet
    self.spin_result = None

    self.max_bet = config.max_bet
    self.payout_delay_secs = config.payout_delay_secs

    self.symbols = []
    self.reels = []
    self.randomizer = randomizer
    self.payout_table = Pay_Table()

    # Set up events
    events = ["state_changed", "spin_completed"]

    self.events = {event: dict() for event in events}

  @property
  def is_spinning(self):
    return self.spin_result is not None

  def add_reel(self, stops):
    """ Add a reel to the machine """

    reel = Reel(index=len(self.reels), stops=stops, randomizer=self.randomizer)
    self.reels.append(reel)

  def register(self, event, who, callback=None):
    """ Register for updates """

    if callback is None:
      callback = getattr(who, 'update')

    self.events[event][who] = callback

  def unregister(self, event, who):
    """ Unregister for updates """

    del self.events[event][who]

  def notify(self, event, message=None):
    """ Notify the subscribers for a particular event """

    for subscriber, callback in self.events[event].iteritems():
      callback(message)

  def payout(self, amount):
    """ Add to the credits """

    self.credits = self.credits + amount
    self.winner_paid = amount

  def place_bet(self):
    """ Place the bet and remove the amount from the credits """

    # You can't bet more than your credits!
    assert self.bet is not None
    assert self.bet > 0
    assert self.credits is not None
    assert self.bet <= self.credits
    self.credits -= self.bet

    self.winner_paid = 0

    self.notify("state_changed")

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
      self.notify("state_changed")

  def decrement_bet(self, message=None):
    """ Decrement the bet by one """

    if self.bet > 1:
      self.bet -= 1
      self.notify("state_changed")

  def spin(self):
    """ Spin the reels """

    assert len(self.reels) > 0

    # Take the bet
    bet = self.place_bet()

    reels = []
    for reel in self.reels:
      reels.append(reel.spin())

    self.spin_result = Spin_Result(reels, winner_paid=None)

  def eval_spin(self):
    """ Evaluate the spin """

    winner_paid = self.payout_table.calculate_payout(
        self.spin_result.reels) * self.bet

    # Add the winnings, if any
    if winner_paid > 0:
      self.payout(winner_paid)

    self.notify("spin_completed", winner_paid)

    self.spin_result = None
