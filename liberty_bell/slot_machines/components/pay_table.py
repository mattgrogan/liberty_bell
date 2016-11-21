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

    for payout in self.payouts:
      if payout.is_match(symbols) and payout.winner_paid > winning_payout:
        winning_payout = payout.winner_paid

    return winning_payout
