from __future__ import print_function

import pytest
import liberty_bell
from liberty_bell.mock import Mock_Random, Mock_Observer

symbols = liberty_bell.Liberty_Bell_Symbols()


def test_liberty_bell_machine():

    # Create the machine
    slot=liberty_bell.Liberty_Bell_Machine()

    payout_table=slot.payout_table

    # Jackpot
    spin_result=[symbols.LIBERTY_BELL,
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
