from __future__ import print_function

import pytest
import liberty_bell

def test_reel():

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

    # Create the reel
    r = liberty_bell.Reel(name="Reel 1", stops=stops)

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
    slot = liberty_bell.Simple_Three_Reel_Machine(name="Machine 1", stops=stops, randomizer=randomizer)

    # Spin
    result = slot.spin()

    assert result[0] == "Liberty Bell"
    assert result[1] == "Heart"
    assert result[2] == "Diamond"
