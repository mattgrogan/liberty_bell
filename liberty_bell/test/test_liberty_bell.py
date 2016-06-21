from __future__ import print_function

import pytest
import liberty_bell

symbols = liberty_bell.Liberty_Bell_Symbols()

def test_reel():

    # Create the reel
    r = liberty_bell.Liberty_Bell_Reel(name="Reel 1", stops=[])

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

    # Create the stops
    stops = ["Liberty Bell",
             "Heart",
             "Diamond",
             "Spade",
             "Spade",
             "Spade",
             "Horseshoe",
             "Horseshoe",
             "Horseshoe",
             "Star"
             ]

    randomizer = liberty_bell.RandomMock()

    # Create the machine
    slot = liberty_bell.Simple_Three_Reel_Machine(
        name="Machine 1", stops=stops, randomizer=randomizer)

    # Spin
    spin_result = slot.spin()

    assert spin_result.reel_symbols[0].name == "Liberty Bell"
    assert spin_result.reel_symbols[1].name == "Heart"
    assert spin_result.reel_symbols[2].name == "Diamond"


def test_sets():

    symbols = ("Liberty Bell",
               "Heart",
               "Diamond",
               "Spade",
               "Horseshoe",
               "Star"
               )

    ORDER_LOOKUP = dict(zip(symbols, range(len(symbols))))

    print(ORDER_LOOKUP)

    # a = ["Liberty Bell", "Liberty Bell", "Liberty Bell"]
    # b = ["Liberty Bell", "Liberty Bell", "Liberty Bell"]
    #
    # print(cmp(ORDER_LOOKUP[a],ORDER_LOOKUP[b]))
    #
    a = ["Horseshoe", "Star", "Horseshoe"]
    b = ["Star", "Horseshoe", "Horseshoe"]

    x = sorted(a, key=ORDER_LOOKUP.get)
    print(x)

    z = sorted(b, key=ORDER_LOOKUP.get)

    assert x == z
    #
    # print(cmp(ORDER_LOOKUP[a],ORDER_LOOKUP[b]))


def test_payout():

    symbols = ("Liberty Bell",
               "Heart",
               "Diamond",
               "Spade",
               "Horseshoe",
               "Star"
               )

    # Create the stops
    stops = ["Liberty Bell",
             "Heart",
             "Diamond",
             "Spade",
             "Spade",
             "Spade",
             "Horseshoe",
             "Horseshoe",
             "Horseshoe",
             "Star"
             ]

    randomizer = liberty_bell.RandomMock(sequence=[0, 0, 0])

    # Create payout table
    payout_table = liberty_bell.Liberty_Bell_Payout()

    # Create the machine
    slot = liberty_bell.Simple_Three_Reel_Machine(
        name="Machine 1", stops=stops, randomizer=randomizer)

    # Spin
    spin_result = slot.spin()

    assert spin_result.reel_symbols[0].name == "Liberty Bell"
    assert spin_result.reel_symbols[1].name == "Liberty Bell"
    assert spin_result.reel_symbols[2].name == "Liberty Bell"

    # Check payout
    assert spin_result.winner_paid == 20
