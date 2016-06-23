from symbols import Symbol
from machine import Slot_Machine
from payout import Payline


class Liberty_Bell_Symbols(object):
    """ An enumerator class to hold all the symbol references """

    def __init__(self):
        """ Initialize the symbols for this game """

        self.LIBERTY_BELL = Symbol(name="Liberty Bell")
        self.HEART = Symbol(name="Heart")
        self.DIAMOND = Symbol(name="Diamond")
        self.SPADE = Symbol(name="Spade")
        self.HORSESHOE = Symbol(name="Horseshoe")
        self.STAR = Symbol(name="Star")


class Liberty_Bell_Machine(Slot_Machine):
    """ A slot machine based on the original Liberty Bell machine """

    def __init__(self, *args, **kwargs):
        """ Initialize the Liberty Bell slot Machine """

        super(Liberty_Bell_Machine, self).__init__(*args, **kwargs)

        self.name = "Liberty Bell"
        self.symbols = Liberty_Bell_Symbols()

        stops = [self.symbols.LIBERTY_BELL, self.symbols.HEART, self.symbols.DIAMOND,
                 self.symbols.SPADE, self.symbols.SPADE, self.symbols.SPADE,
                 self.symbols.HORSESHOE, self.symbols.HORSESHOE, self.symbols.HORSESHOE,
                 self.symbols.STAR]

        # Add three reels with identical stops
        for i in range(3):
            self.add_reel(name="Reel %i" % (i + 1), stops=stops)

        # Add the paylines to the payout table
        self.payout_table.append(Payline({self.symbols.LIBERTY_BELL: 3}, 20))
        self.payout_table.append(Payline({self.symbols.HEART: 3}, 16))
        self.payout_table.append(Payline({self.symbols.DIAMOND: 3}, 12))
        self.payout_table.append(Payline({self.symbols.SPADE: 3}, 8))
        self.payout_table.append(
            Payline({self.symbols.HORSESHOE: 2, self.symbols.STAR: 1}, 4))
        self.payout_table.append(Payline({self.symbols.HORSESHOE: 2}, 2))
