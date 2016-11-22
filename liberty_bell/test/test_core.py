from __future__ import print_function

import sys

import pytest

from liberty_bell.main_controller import Main_Controller
from liberty_bell.mock import Mock_Observer, Mock_Random
from liberty_bell.slot_machine_menu_item import Slot_Machine_Menu_Item
from liberty_bell.slot_machines.components.payline import Payline
from liberty_bell.slot_machines.components.symbol import Symbol
from liberty_bell.slot_machines.gold_award_machine import Gold_Award_Machine
from liberty_bell.slot_machines.liberty_bell_machine import (Liberty_Bell_Machine,
                                                             Slot_Machine)


def test_slot_machine():

  print(sys.path)

  slot_machine = Slot_Machine()

  assert slot_machine.name == "Slot Machine"

  # Test initialization
  slot_machine.credits == 15
  slot_machine.bet == 1
  slot_machine.max_bet = 10

  # Test spin with no reels
  with pytest.raises(Exception):
    result = slot_machine.spin()

  # Test the betting functions
  slot_machine.increment_bet()
  assert slot_machine.bet == 2
  slot_machine.decrement_bet()
  assert slot_machine.bet == 1

  # Test max and min bets
  for i in range(slot_machine.max_bet + 1):
    slot_machine.increment_bet()
  assert slot_machine.bet == 10

  for i in range(slot_machine.bet + 1):
    slot_machine.decrement_bet()
  assert slot_machine.bet == 1

  # Test that you cannot bet more than your credits
  slot_machine.credits = 2
  slot_machine.increment_bet()  # bet=2
  slot_machine.increment_bet()  # bet=3 (nope!)
  assert slot_machine.bet == 2


def test_machine_betting():

  mock_random = Mock_Random()
  slot_machine = Slot_Machine(randomizer=mock_random)

  symbols = []
  for i in range(3):
    symbols.append(Symbol("Symbol %i" % i))

  assert len(symbols) == 3

  reels = []
  for j in range(3):
    slot_machine.add_reel(symbols)

  assert len(slot_machine.reels) == 3


def test_reel():

  # The reels will move through this sequence of stops
  mock_random = Mock_Random(sequence=[0, 1, 0, 2])
  slot_machine = Slot_Machine(randomizer=mock_random)
  slot_machine.credits = 100
  slot_machine.bet = 1

  symbols = []
  for i in range(3):
    symbols.append(Symbol("Symbol %i" % i))

  reels = []
  for j in range(3):
    slot_machine.add_reel(symbols)

  assert len(slot_machine.reels[0].stops) == 3
  assert len(slot_machine.reels[1].stops) == 3
  assert len(slot_machine.reels[2].stops) == 3

  slot_machine.spin()
  assert slot_machine.spin_result.reels[0] == symbols[0]
  assert slot_machine.spin_result.reels[1] == symbols[1]
  assert slot_machine.spin_result.reels[2] == symbols[0]

  slot_machine.spin()
  assert slot_machine.spin_result.reels[0] == symbols[2]
  assert slot_machine.spin_result.reels[1] == symbols[0]
  assert slot_machine.spin_result.reels[2] == symbols[1]


def test_payout():

  # The reels will move through this sequence of stops
  winning_seq = [0, 0, 0,
                 1, 1, 1,
                 2, 2, 1,
                 2, 1, 2,
                 1, 2, 2,
                 2, 2, 2,
                 ]

  mock_random = Mock_Random(sequence=winning_seq)
  slot_machine = Slot_Machine(randomizer=mock_random)
  slot_machine.credits = 100
  slot_machine.bet = 1

  symbols = []
  for i in range(3):
    symbols.append(Symbol("Symbol %i" % i))

  reels = []
  for j in range(3):
    slot_machine.add_reel(symbols)

  # Add paylines
  # First symbol, three times, pays three
  slot_machine.payout_table.append(Payline({symbols[0]: 3}, 3))

  # Second symbol, three times, pays two
  slot_machine.payout_table.append(Payline({symbols[1]: 3}, 2))

  # Third symbol, three times, pays one
  slot_machine.payout_table.append(Payline({symbols[2]: 2}, 1))

  expected_results = [3, 2, 1, 1, 1, 1]
  expected_credits = 100

  for result in expected_results:
    slot_machine.spin()
    slot_machine.eval_spin()
    assert slot_machine.winner_paid == result
    expected_credits = expected_credits - 1 + result
    assert slot_machine.credits == expected_credits


def test_losing_paylines():
  # The reels will move through this sequence of stops

  losing_seq = [1, 0, 0,
                1, 0, 1,
                0, 2, 1,
                2, 1, 0,
                0, 0, 2,
                2, 1, 1,
                ]

  mock_random = Mock_Random(sequence=losing_seq)
  slot_machine = Slot_Machine(randomizer=mock_random)
  slot_machine.credits = 100
  slot_machine.bet = 1

  symbols = []
  for i in range(3):
    symbols.append(Symbol("Symbol %i" % i))

  reels = []
  for j in range(3):
    slot_machine.add_reel(symbols)
