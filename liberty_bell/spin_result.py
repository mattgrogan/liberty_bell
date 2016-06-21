class Spin_Result(object):
    """ Holds the results of a spin """

    def __init__(self, reels, winner_paid):
        """ Initialize the result """

        self.reels = reels
        self.winner_paid = winner_paid
