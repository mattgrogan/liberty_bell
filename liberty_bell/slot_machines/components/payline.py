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
