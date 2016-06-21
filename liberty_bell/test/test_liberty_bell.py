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
