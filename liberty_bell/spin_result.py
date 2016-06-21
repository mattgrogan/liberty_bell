class Spin_Result(object):
    """ Holds the results of a spin """

    def __init__(self, reels, winner_paid):
        """ Initialize the result """

        self.reels = reels
        self.winner_paid = winner_paid

    def __str__(self):
        """ Convert to a string """

        result = "Payout: %i [" % self.winner_paid
        result += ' | '.join(str(r) for r in self.reels)
        result += " ]"

        return result
