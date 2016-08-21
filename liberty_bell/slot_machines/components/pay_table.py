class Pay_Table(object):
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
