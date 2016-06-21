from symbols import Liberty_Bell_Symbols

symbols = Liberty_Bell_Symbols()


class Liberty_Bell_Payout(object):
    """ Three Liberty Bells """

    def __init__(self):
        """ Initialize the payout """

        self.symbols = [symbols.LIBERTY_BELL,
                        symbols.LIBERTY_BELL,
                        symbols.LIBERTY_BELL]
        self.winner_paid = 20

    def is_match(self, candidate):
        """ Check if symbols is a match """

        return all(self.symbols[i] == candidate[i] for i in range(len(candidate)))


class Heart_Payout(object):
    """ Three Hearts """

    def __init__(self):
        """ Initialize the payout """

        self.symbols = [symbols.HEART,
                        symbols.HEART,
                        symbols.HEART]
        self.winner_paid = 16

    def is_match(self, candidate):
        """ Check if symbols is a match """

        return all(self.symbols[i] == candidate[i] for i in range(len(candidate)))


class Diamond_Payout(object):
    """ Three Diamonds """

    def __init__(self):
        """ Initialize the payout """

        self.symbols = [symbols.DIAMOND,
                        symbols.DIAMOND,
                        symbols.DIAMOND]
        self.winner_paid = 12

    def is_match(self, candidate):
        """ Check if symbols is a match """

        return all(self.symbols[i] == candidate[i] for i in range(len(candidate)))


class Spade_Payout(object):
    """ Three Spades """

    def __init__(self):
        """ Initialize the payout """

        self.symbols = [symbols.SPADE,
                        symbols.SPADE,
                        symbols.SPADE]
        self.winner_paid = 8

    def is_match(self, candidate):
        """ Check if symbols is a match """

        return all(self.symbols[i] == candidate[i] for i in range(len(candidate)))


class Horseshoe_Star_Payout(object):
    """ Two horseshoes and one star """

    def __init__(self):
        """ Initialize the payout """

        self.symbols = [symbols.HORSESHOE,
                        symbols.HORSESHOE,
                        symbols.STAR]
        self.winner_paid = 4

    def is_match(self, candidate):
        """ Check if symbols is a match """

        return all(sorted(self.symbols)[i] == sorted(candidate)[i] for i in range(len(candidate)))

class Horseshoe_Payout(object):
    """ Two horseshoes """

    def __init__(self):
        """ Initialize the payout """

        self.symbol = symbols.HORSESHOE
        self.winner_paid = 2

    def is_match(self, candidate):
        """ Check if symbols is a match """

        count = 0

        for i in range(len(candidate)):
            if candidate[i] == self.symbol:
                count = count + 1

        return count >= 2

class Liberty_Bell_Payout_Table(object):
    """ Class to hold the payout table """

    def __init__(self):
        """ Initialize the payout table """

        self.name = "Liberty Bell Payout Table"
        self.payouts = [Liberty_Bell_Payout(), Heart_Payout(),
            Diamond_Payout(), Spade_Payout(), Horseshoe_Star_Payout(),
            Horseshoe_Payout()]

    def calculate_payout(self, symbols):
        """ Check if symbols is a winner! """

        i = 0
        winning_payout = 0

        while winning_payout == 0 and i < len(self.payouts):
            payout = self.payouts[i]
            if payout.is_match(symbols):
                winning_payout = payout.winner_paid
            i = i + 1

        return winning_payout
