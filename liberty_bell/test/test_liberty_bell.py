from __future__ import print_function

import pytest
import liberty_bell
from liberty_bell.mock import MockRandom

symbols = liberty_bell.Liberty_Bell_Symbols()






def test_reel():

    randomizer = MockRandom()

    # Create the reel
    slot = liberty_bell.Liberty_Bell_Machine(randomizer=randomizer)
    r = slot.reels[0]

    stops = r.stops

    assert(str(r) == "Reel 1")
    assert(r.stops == stops)
    assert len(r.stops) == 10

    for stop in stops:
        # Spin the reel
        result = r.spin()
        assert result == stop

    # Make sure that the mock will cycle through
    result = r.spin()
    assert result == stops[0]


def test_machine():

    randomizer = MockRandom()

    # Create the machine
    slot = liberty_bell.Liberty_Bell_Machine(randomizer=randomizer)

    # Set up the initial credits and bet
    slot.initialize(100, 1)

    assert slot.credits == 100

    # Spin
    spin_result = slot.spin()

    assert spin_result.reels[0].name == "Liberty Bell"
    assert spin_result.reels[1].name == "Heart"
    assert spin_result.reels[2].name == "Diamond"
    assert spin_result.winner_paid == 0

    assert slot.credits == 99


def test_payout():

    randomizer = MockRandom(sequence=[0, 0, 0])

    # Create payout table
    payout_table = liberty_bell.Payline({symbols.LIBERTY_BELL: 3}, 20)

    # Create the machine
    slot = liberty_bell.Liberty_Bell_Machine(randomizer=randomizer)
    # Set up the initial credits and bet
    slot.initialize(100, 1)

    assert slot.credits == 100

    # Spin
    spin_result = slot.spin()

    assert spin_result.reels[0].name == "Liberty Bell"
    assert spin_result.reels[1].name == "Liberty Bell"
    assert spin_result.reels[2].name == "Liberty Bell"

    # Check payout
    assert spin_result.winner_paid == 20

    assert slot.credits == 119

    slot.increment_bet()
    slot.increment_bet()
    slot.increment_bet()

    # Spin
    spin_result = slot.spin()

    assert spin_result.reels[0].name == "Liberty Bell"
    assert spin_result.reels[1].name == "Liberty Bell"
    assert spin_result.reels[2].name == "Liberty Bell"

    # Check payout
    assert spin_result.winner_paid == 80  # Bet 4

    assert slot.credits == 195  # spent 5

    slot.decrement_bet()

    # Spin
    spin_result = slot.spin()

    assert spin_result.reels[0].name == "Liberty Bell"
    assert spin_result.reels[1].name == "Liberty Bell"
    assert spin_result.reels[2].name == "Liberty Bell"

    # Check payout
    assert spin_result.winner_paid == 60

    assert slot.credits == 252

    # make sure we can't decrement below zero
    slot.decrement_bet()
    slot.decrement_bet()
    slot.decrement_bet()
    slot.decrement_bet()
    slot.decrement_bet()
    slot.decrement_bet()
    slot.decrement_bet()

    # Spin
    spin_result = slot.spin()

    assert spin_result.reels[0].name == "Liberty Bell"
    assert spin_result.reels[1].name == "Liberty Bell"
    assert spin_result.reels[2].name == "Liberty Bell"

    # Check payout
    assert spin_result.winner_paid == 20

    assert slot.credits == 271

    # make sure we can't increment past max bet
    for i in range(40):
        slot.increment_bet()

    # Spin
    spin_result = slot.spin()

    assert spin_result.reels[0].name == "Liberty Bell"
    assert spin_result.reels[1].name == "Liberty Bell"
    assert spin_result.reels[2].name == "Liberty Bell"

    # Check payout
    assert spin_result.winner_paid == 200

    assert slot.credits == 461


def test_payout_table():

    # Create the machine
    slot = liberty_bell.Liberty_Bell_Machine()

    payout_table = slot.payout_table

    # Jackpot
    spin_result = [symbols.LIBERTY_BELL,
                   symbols.LIBERTY_BELL,
                   symbols.LIBERTY_BELL]

    result = payout_table.calculate_payout(spin_result)

    assert result == 20

    # no winner
    spin_result = [symbols.STAR,
                   symbols.LIBERTY_BELL,
                   symbols.LIBERTY_BELL]

    result = payout_table.calculate_payout(spin_result)

    assert result == 0

    # Hearts
    spin_result = [symbols.HEART,
                   symbols.HEART,
                   symbols.HEART]

    result = payout_table.calculate_payout(spin_result)

    assert result == 16

    # Diamond
    spin_result = [symbols.DIAMOND,
                   symbols.DIAMOND,
                   symbols.DIAMOND]

    result = payout_table.calculate_payout(spin_result)

    assert result == 12

    # Spade
    spin_result = [symbols.SPADE,
                   symbols.SPADE,
                   symbols.SPADE]

    result = payout_table.calculate_payout(spin_result)

    assert result == 8

    # Horseshoe + star
    spin_result = [symbols.HORSESHOE,
                   symbols.HORSESHOE,
                   symbols.STAR]

    result = payout_table.calculate_payout(spin_result)

    assert result == 4

    spin_result = [symbols.HORSESHOE,
                   symbols.STAR,
                   symbols.HORSESHOE]

    result = payout_table.calculate_payout(spin_result)

    assert result == 4

    spin_result = [symbols.STAR,
                   symbols.HORSESHOE,
                   symbols.HORSESHOE]

    result = payout_table.calculate_payout(spin_result)

    assert result == 4

    # Two horseshoes
    spin_result = [symbols.HORSESHOE,
                   symbols.HORSESHOE,
                   symbols.HORSESHOE]

    result = payout_table.calculate_payout(spin_result)

    assert result == 2

    spin_result = [symbols.HORSESHOE,
                   symbols.SPADE,
                   symbols.HORSESHOE]

    result = payout_table.calculate_payout(spin_result)

    assert result == 2
