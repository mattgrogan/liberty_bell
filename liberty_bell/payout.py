from collections import defaultdict


class Payline(object):
    """ A winning combination! """

    def __init__(self, rule, winner_paid):
        """ Pass rule as a dict with the symbol and required number of occurrences """

        self.rule = {}
        self.winner_paid = winner_paid

        for symbol, minimum_occurrence in rule.iteritems():
            self.rule[str(symbol)] = minimum_occurrence  # index by string only

    def is_match(self, candidate):
        """ Candidate is a list of symbols. Check if they match this payout rule """

        candidate_dict = defaultdict(int)
        for symbol in candidate:
            candidate_dict[str(symbol)] += 1

        match = True

        for symbol in self.rule:
            if candidate_dict[symbol] < self.rule[symbol]:
                match = False
                break

        return match


class Payout_Table(object):
    """ Class to hold the payout table """

    def __init__(self, name="Payout Table"):
        """ Initialize the payout table """

        self.name = name
        self.payouts = []

    def append(self, payline):
        """ Add a payline to the table. Pass a dictionary with the symbols. Must be ordered. """

        self.payouts.append(payline)

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
