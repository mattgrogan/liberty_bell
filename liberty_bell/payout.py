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


class Liberty_Bell_Payout_Table(object):
    """ Class to hold the payout table """

    def __init__(self):
        """ Initialize the payout table """

        self.name = "Liberty Bell Payout Table"
        self.payouts = [Liberty_Bell_Payout()]

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
