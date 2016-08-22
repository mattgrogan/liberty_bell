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

    self.name = "Slot Machine"
    self.credits = None
    self.bet = None

    config = Config()
    self.max_bet = config.max_bet
    self.payout_delay_secs = config.payout_delay_secs

    self.symbols = []
    self.reels = []
    self.randomizer = randomizer
    self.payout_table = Pay_Table()

    # Set up events
    events = ["credits_changed", "winner_paid_changed",
              "amount_bet_changed", "spin_completed",
              "enable_spin", "disable_spin",
              "enable_increase_bet", "disable_increase_bet",
              "enable_decrease_bet", "disable_decrease_bet"]

    self.events = {event: dict() for event in events}

    # Register for events
    self.register("amount_bet_changed", self, self.handle_state_change)
    self.register("credits_changed", self, self.handle_state_change)
    self.register("spin_completed", self, self.handle_state_change)

  def add_reel(self, stops):
    """ Add a reel to the machine """

    reel = Reel(index=len(self.reels), stops=stops, randomizer=self.randomizer)
    self.reels.append(reel)

  def initialize(self, credits=None, bet=None):
    """ Initialize credit and/or bet values """

    if credits is not None:
      self.credits = credits
      self.notify("credits_changed", self.credits)

    if bet is not None:
      self.bet = bet
      self.notify("amount_bet_changed", bet)

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

    for i in range(amount):
      self.credits = self.credits + 1
      self.notify("winner_paid_changed", i + 1)
      self.notify("credits_changed", self.credits)
      time.sleep(self.payout_delay_secs)

  def place_bet(self):
    """ Place the bet and remove the amount from the credits """

    # You can't bet more than your credits!
    assert self.bet is not None
    assert self.bet > 0
    assert self.credits is not None
    assert self.bet <= self.credits
    self.credits -= self.bet

    self.notify("credits_changed", self.credits)

    return self.bet

  def handle_state_change(self, message=None):
    """ Handle any changes to the bet and raise events when we hit the min or max """

    bet_is_below_credits = self.bet < self.credits
    has_enough_credits = self.bet <= self.credits
    below_max_bet = self.bet < self.max_bet
    at_least_one_credit_bet = self.bet > 1

    # Can we increase the bet?
    if below_max_bet and bet_is_below_credits:
      self.notify("enable_increase_bet")
    else:
      self.notify("disable_increase_bet")

    # Can we decrease the bet?
    if at_least_one_credit_bet:
      self.notify("enable_decrease_bet")
    else:
      self.notify("disable_decrease_bet")

    # Can we spin?
    if has_enough_credits:
      self.notify("enable_spin")
    else:
      self.notify("disable_spin")

  def increment_bet(self, message=None):
    """ Increment the bet by one """

    attempted_bet = self.bet + 1

    if attempted_bet <= self.credits and attempted_bet <= self.max_bet:
      self.bet = attempted_bet
      self.notify("amount_bet_changed", self.bet)

  def decrement_bet(self, message=None):
    """ Decrement the bet by one """

    if self.bet > 1:
      self.bet -= 1
      self.notify("amount_bet_changed", self.bet)

  def spin(self):
    """ Spin the reels """

    assert len(self.reels) > 0

    # Take the bet
    bet = self.place_bet()

    reels = []
    for reel in self.reels:
      reels.append(reel.spin())

    spin_result = Spin_Result(reels, winner_paid=None)

    return spin_result

  def eval_spin(self, spin):
    """ Evaluate the spin """

    winner_paid = self.payout_table.calculate_payout(spin.reels) * self.bet

    # Add the winnings, if any
    if winner_paid > 0:
      self.payout(winner_paid)

    self.notify("spin_completed", winner_paid)
