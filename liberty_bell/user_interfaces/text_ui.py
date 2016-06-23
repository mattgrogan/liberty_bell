from __future__ import print_function

import sys
sys.path.append("..")

from liberty_bell.events import Events
from liberty_bell.ui import Slot_UI


class Slot_Text_UI(Slot_UI):
    """ Prototype Text UI for the slot machine """

    def __init__(self, *args, **kwargs):
        """ Initialize the UI """

        super(Slot_Text_UI, self).__init__(*args, **kwargs)

        self.credits = 0
        self.bet = 0
        self.winner_paid = 0

    def mainloop(self):
        """ The main loop for the game """

        continue_playing = True

        while (continue_playing):
            text = "Choose an option: S: Spin | I: increase bet | D: decrease bet | Q: quit [S] "
            option = raw_input(text)

            if option == ["S", "s"]:
                self.on_spin_press()
            elif option == ["I", "i"]:
                self.on_increment_bet_press()
            elif option in ["D", "d"]:
                self.on_decrement_bet_press()
            elif option in ["Q", "q"]:
                continue_playing = False
            else:
                self.on_spin_press()

            print("\n")

    def print_status(self):
        """ Print the status on one line """
        print("Credits: %i | Bet: %i | Winner paid: %i " %
              (self.credits, self.bet, self.winner_paid))

    def update_credits(self, credits):
        """ Update the credits box """

        self.credits = credits
        self.print_status()

    def update_bet(self, bet):
        """ Update the bet """

        self.bet = bet
        self.print_status

    def update_winner_paid(self, winner_paid):
        """ Print the amount paid """

        self.winner_paid = winner_paid
        self.print_status

    def update_reel(self, reel, symbol):
        """ Update reel with the result """

        print("Reel %i: %s" % (reel, symbol))
