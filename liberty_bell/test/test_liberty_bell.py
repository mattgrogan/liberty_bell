from __future__ import print_function

import pytest
import liberty_bell

symbols = liberty_bell.Liberty_Bell_Symbols()


def test_reel():

    # Create the reel
    r = liberty_bell.Liberty_Bell_Reel(name="Reel 1")

    stops = r.stops

    assert(str(r) == "Reel 1")
    assert(r.stops == stops)
    assert len(r.stops) == 10

    # Set a deterministic randomizer
    randomizer = liberty_bell.RandomMock()
    r.set_randomizer(randomizer)

    for stop in stops:
        # Spin the reel
        result = r.spin()
        assert result == stop

    # Make sure that the mock will cycle through
    result = r.spin()
    assert result == stops[0]


def test_machine():

    randomizer = liberty_bell.RandomMock()

    # Create the machine
    slot = liberty_bell.Liberty_Bell_Machine(
        name="Machine 1", randomizer=randomizer)

    assert slot.credits == 100

    # Spin
    spin_result = slot.spin(bet = 1)

    assert spin_result.reels[0].name == "Liberty Bell"
    assert spin_result.reels[1].name == "Heart"
    assert spin_result.reels[2].name == "Diamond"
    assert spin_result.winner_paid == 0

    assert slot.credits == 99

def test_payout():

    randomizer = liberty_bell.RandomMock(sequence=[0, 0, 0])

    # Create payout table
    payout_table = liberty_bell.Liberty_Bell_Payout()

    # Create the machine
    slot = liberty_bell.Liberty_Bell_Machine(
        name="Machine 1", randomizer=randomizer)

    assert slot.credits == 100

    # Spin
    spin_result = slot.spin(bet=1)

    assert spin_result.reels[0].name == "Liberty Bell"
    assert spin_result.reels[1].name == "Liberty Bell"
    assert spin_result.reels[2].name == "Liberty Bell"

    # Check payout
    assert spin_result.winner_paid == 20

    assert slot.credits == 119

    # Spin
    spin_result = slot.spin(bet=2)

    assert spin_result.reels[0].name == "Liberty Bell"
    assert spin_result.reels[1].name == "Liberty Bell"
    assert spin_result.reels[2].name == "Liberty Bell"

    # Check payout
    assert spin_result.winner_paid == 40

    assert slot.credits == 157 # bet 2

def test_payout_table():

    payout_table = liberty_bell.Liberty_Bell_Payout_Table()

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
