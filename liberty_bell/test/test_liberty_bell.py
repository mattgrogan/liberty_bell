from __future__ import print_function

import pytest
import liberty_bell

def test_reel():

    r = liberty_bell.Reel()

    assert str(r) == "X"
