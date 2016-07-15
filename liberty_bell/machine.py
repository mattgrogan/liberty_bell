import random
import time

from events import Events
from payout import Payline, Payout_Table
from reel import Reel
from spin_result import Spin_Result

MAX_BET = 10
PAYOUT_DELAY_SECS = 0.20


class Slot_Machine(object):
  """ A superclass for slot machines """

  def __init__(self, randomizer=random):
    """ Initialize the machine """

    self.name = "Slot Machine"
    self.credits = None
    self.bet = None
    self.max_bet = MAX_BET
    self.symbols = []
    self.reels = []
    self.randomizer = randomizer
    self.payout_table = Payout_Table()

    # Set up events
    events = [Events.CREDITS_CHANGED, Events.PAYOUT,
              Events.PLACE_BET, Events.BET_CHANGED,
              Events.SPIN_EVAL]

    self.events = {event: dict() for event in events}

  def add_reel(self, stops):
    """ Add a reel to the machine """

    reel = Reel(index=len(self.reels), stops=stops, randomizer=self.randomizer)
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

    for i in range(amount):
      self.credits = self.credits + 1
      self.notify(Events.PAYOUT, i + 1)
      self.notify(Events.CREDITS_CHANGED, self.credits)
      time.sleep(PAYOUT_DELAY_SECS)

  def place_bet(self):
    """ Place the bet and remove the amount from the credits """

    # You can't bet more than your credits!
    assert self.bet is not None
    assert self.bet > 0
    assert self.credits is not None
    assert self.bet <= self.credits
    self.credits -= self.bet

    self.notify(Events.PLACE_BET, self.bet)
    self.notify(Events.CREDITS_CHANGED, self.credits)

    return self.bet

  def increment_bet(self, message=None):
    """ Increment the bet by one """

    if (self.bet + 1) > self.credits:
      raise ValueError("Not enough credits")

    if self.bet < self.max_bet:
      self.bet += 1
      self.notify(Events.BET_CHANGED, self.bet)

  def decrement_bet(self, message=None):
    """ Decrement the bet by one """

    if self.bet > 1:
      self.bet -= 1
      self.notify(Events.BET_CHANGED, self.bet)

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

    self.notify(Events.SPIN_EVAL, winner_paid)
