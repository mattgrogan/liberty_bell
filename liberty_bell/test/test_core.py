from __future__ import print_function

import pytest
import liberty_bell
from liberty_bell.mock import Mock_Random, Mock_Observer


def test_slot_machine():

    slot_machine = liberty_bell.Slot_Machine()

    assert slot_machine.name == "Slot Machine"

    # Test initialization
    slot_machine.initialize(credits=15, bet=1)
    assert slot_machine.credits == 15
    assert slot_machine.bet == 1

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
    slot_machine.initialize(credits=2)
    slot_machine.increment_bet()
    with pytest.raises(ValueError):
        slot_machine.increment_bet()

    # Test that the bet change event is fired
    mock_increment = liberty_bell.mock.Mock_Observer()
    slot_machine.initialize(credits=100, bet=1)
    slot_machine.register(liberty_bell.Events.BET_CHANGED,
                          mock_increment, mock_increment.observe)

    assert mock_increment.fired == False
    slot_machine.increment_bet()
    assert mock_increment.fired == True
    assert mock_increment.message == 2


def test_machine_betting():

    mock_random = liberty_bell.mock.Mock_Random()
    slot_machine = liberty_bell.Slot_Machine(randomizer=mock_random)

    symbols = []
    for i in range(3):
        symbols.append(liberty_bell.Symbol("Symbol %i" % i))

    assert len(symbols) == 3

    reels = []
    for j in range(3):
        slot_machine.add_reel("Reel %i" % j, symbols)

    assert len(slot_machine.reels) == 3

    # Don't forget we have to initialize and put some money in!
    with pytest.raises(AssertionError):
        spin_result = slot_machine.spin()

    # Set up the observers
    observe_credits = liberty_bell.mock.Mock_Observer()
    slot_machine.register(liberty_bell.Events.CREDITS_CHANGED,
                          observe_credits, observe_credits.observe)
    observe_payout = liberty_bell.mock.Mock_Observer()
    slot_machine.register(liberty_bell.Events.PAYOUT,
                          observe_payout, observe_payout.observe)
    observe_place_bet = liberty_bell.mock.Mock_Observer()
    slot_machine.register(liberty_bell.Events.PLACE_BET,
                          observe_place_bet, observe_place_bet.observe)

    slot_machine.initialize(credits=100, bet=1)
    assert observe_credits.fired == True
    observe_credits.reset()
    assert observe_payout.fired == False
    assert observe_place_bet.fired == False

    spin_result = slot_machine.spin()
    assert slot_machine.credits == 99
    assert spin_result.winner_paid == 0

    # Events
    assert observe_credits.fired == True
    assert observe_credits.message == 99
    assert observe_payout.fired == False
    assert observe_place_bet.fired == True
    assert observe_place_bet.message == 1

    observe_credits.reset()
    observe_payout.reset()
    observe_place_bet.reset()

    slot_machine.increment_bet()
    spin_result == slot_machine.spin()
    assert slot_machine.credits == 97

    assert observe_place_bet.fired == True
    assert observe_place_bet.message == 2


def test_reel():

    # The reels will move through this sequence of stops
    mock_random = liberty_bell.mock.Mock_Random(sequence=[0, 1, 0, 2])
    slot_machine = liberty_bell.Slot_Machine(randomizer=mock_random)
    slot_machine.initialize(credits=100, bet=1)

    symbols = []
    for i in range(3):
        symbols.append(liberty_bell.Symbol("Symbol %i" % i))

    reels = []
    for j in range(3):
        slot_machine.add_reel("Reel %i" % j, symbols)

    assert len(slot_machine.reels[0].stops) == 3
    assert len(slot_machine.reels[1].stops) == 3
    assert len(slot_machine.reels[2].stops) == 3

    spin_result = slot_machine.spin()
    assert spin_result.reels[0] == symbols[0]
    assert spin_result.reels[1] == symbols[1]
    assert spin_result.reels[2] == symbols[0]

    spin_result = slot_machine.spin()
    assert spin_result.reels[0] == symbols[2]
    assert spin_result.reels[1] == symbols[0]
    assert spin_result.reels[2] == symbols[1]


def test_payout():

    # The reels will move through this sequence of stops
    winning_seq = [0, 0, 0,
                   1, 1, 1,
                   2, 2, 1,
                   2, 1, 2,
                   1, 2, 2,
                   2, 2, 2,
                   ]

    mock_random = liberty_bell.mock.Mock_Random(sequence=winning_seq)
    slot_machine = liberty_bell.Slot_Machine(randomizer=mock_random)
    slot_machine.initialize(credits=100, bet=1)

    symbols = []
    for i in range(3):
        symbols.append(liberty_bell.Symbol("Symbol %i" % i))

    reels = []
    for j in range(3):
        slot_machine.add_reel("Reel %i" % j, symbols)

    # Set up the observers
    observe_credits = liberty_bell.mock.Mock_Observer()
    slot_machine.register(liberty_bell.Events.CREDITS_CHANGED,
                          observe_credits, observe_credits.observe)
    observe_payout = liberty_bell.mock.Mock_Observer()
    slot_machine.register(liberty_bell.Events.PAYOUT,
                          observe_payout, observe_payout.observe)
    observe_place_bet = liberty_bell.mock.Mock_Observer()
    slot_machine.register(liberty_bell.Events.PLACE_BET,
                          observe_place_bet, observe_place_bet.observe)

    # Add paylines
    # First symbol, three times, pays three
    slot_machine.payout_table.append(liberty_bell.Payline({symbols[0]: 3}, 3))

    # Second symbol, three times, pays two
    slot_machine.payout_table.append(liberty_bell.Payline({symbols[1]: 3}, 2))

    # Third symbol, three times, pays one
    slot_machine.payout_table.append(liberty_bell.Payline({symbols[2]: 2}, 1))

    expected_results = [3, 2, 1, 1, 1, 1]
    expected_credits = 100

    for result in expected_results:
        spin_result = slot_machine.spin()
        assert spin_result.winner_paid == result
        expected_credits = expected_credits - 1 + result
        # Check events
        assert slot_machine.credits == expected_credits
        assert observe_payout.fired == True
        assert observe_payout.message == result
        observe_payout.reset()


def test_losing_paylines():
    # The reels will move through this sequence of stops

    losing_seq = [1, 0, 0,
                  1, 0, 1,
                  0, 2, 1,
                  2, 1, 0,
                  0, 0, 2,
                  2, 1, 1,
                  ]

    mock_random = liberty_bell.mock.Mock_Random(sequence=losing_seq)
    slot_machine = liberty_bell.Slot_Machine(randomizer=mock_random)
    slot_machine.initialize(credits=100, bet=1)

    symbols = []
    for i in range(3):
        symbols.append(liberty_bell.Symbol("Symbol %i" % i))

    reels = []
    for j in range(3):
        slot_machine.add_reel("Reel %i" % j, symbols)

    # Set up the observers
    observe_credits = liberty_bell.mock.Mock_Observer()
    slot_machine.register(liberty_bell.Events.CREDITS_CHANGED,
                          observe_credits, observe_credits.observe)
    observe_payout = liberty_bell.mock.Mock_Observer()
    slot_machine.register(liberty_bell.Events.PAYOUT,
                          observe_payout, observe_payout.observe)
    observe_place_bet = liberty_bell.mock.Mock_Observer()
    slot_machine.register(liberty_bell.Events.PLACE_BET,
                          observe_place_bet, observe_place_bet.observe)

    # Add paylines
    # First symbol, three times, pays three
    slot_machine.payout_table.append(liberty_bell.Payline({symbols[0]: 3}, 3))

    # Second symbol, three times, pays two
    slot_machine.payout_table.append(liberty_bell.Payline({symbols[1]: 3}, 2))

    # Third symbol, three times, pays one
    slot_machine.payout_table.append(liberty_bell.Payline({symbols[2]: 2}, 1))

    expected_credits = 100

    for i in range(len(losing_seq) / 3):
        spin_result = slot_machine.spin()
        assert spin_result.winner_paid == 0
        expected_credits = expected_credits - 1
        assert slot_machine.credits == expected_credits

        # Check events
        assert observe_payout.fired == False
        assert observe_credits.fired == True
        assert observe_place_bet.fired == True
        observe_payout.reset()
        observe_credits.reset()
        observe_place_bet.reset()

def test_ui():

    ui = liberty_bell.Slot_UI()

    observe_spin = liberty_bell.mock.Mock_Observer()
    ui.register(liberty_bell.Events.SPIN,
                          observe_spin, observe_spin.observe)

    observe_increment_bet = liberty_bell.mock.Mock_Observer()
    ui.register(liberty_bell.Events.INCREMENT_BET,
                          observe_increment_bet, observe_increment_bet.observe)

    observe_decrement_bet = liberty_bell.mock.Mock_Observer()
    ui.register(liberty_bell.Events.DECREMENT_BET,
                          observe_decrement_bet, observe_decrement_bet.observe)

    ui.on_spin_press()

    assert observe_spin.fired == True
    assert observe_increment_bet.fired == False
    assert observe_decrement_bet.fired == False

    observe_spin.reset()
    observe_increment_bet.reset()
    observe_decrement_bet.reset()

    ui.on_decrement_bet_press()

    assert observe_spin.fired == False
    assert observe_increment_bet.fired == False
    assert observe_decrement_bet.fired == True

    observe_spin.reset()
    observe_increment_bet.reset()
    observe_decrement_bet.reset()

    ui.on_increment_bet_press()

    assert observe_spin.fired == False
    assert observe_increment_bet.fired == True
    assert observe_decrement_bet.fired == False

    observe_spin.reset()
    observe_increment_bet.reset()
    observe_decrement_bet.reset()
