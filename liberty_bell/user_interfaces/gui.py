import Tkinter as tk
from events import Events
from ui import Slot_UI


class Slot_GUI(Slot_UI, tk.Tk):
    """ Prototype GUI for the slot machine """

    def __init__(self, *args, **kwargs):
        """ Initialize the GUI """

        super(Slot_GUI, self).__init__(*args, **kwargs)
        tk.Tk.__init__(self, *args, **kwargs)

        # Add the buttons
        self.button = tk.Button(self, text="SPIN", command=self.on_spin_press)
        self.button.pack(side=tk.RIGHT)

        self.increment_bet_button = tk.Button(
            self, text="+1", command=self.on_increment_bet_press)
        self.increment_bet_button.pack(side=tk.RIGHT)

        self.decrement_bet_button = tk.Button(
            self, text="-1", command=self.on_decrement_bet_press)
        self.decrement_bet_button.pack(side=tk.RIGHT)

        # Add the text boxes
        self.winner_paid_label = tk.Label(self, text="Winner paid: 0")
        self.winner_paid_label.pack()

        self.credits_label = tk.Label(self, text="Credits: 0")
        self.credits_label.pack()

        self.bet_label = tk.Label(self, text="Bet: 0")
        self.bet_label.pack()

        # Add the reels
        nbr_reels = 3  # TODO: Communicate this info from the machine
        self.reel_labels = []
        for i in range(nbr_reels):
            reel_label = tk.Label(self, text="Reel %i: " % i)
            reel_label.pack()
            self.reel_labels.append(reel_label)

    def update_credits(self, credits):
        """ Update the credits box """

        self.credits_label.configure(text="Credits: %i" % credits)

    def update_bet(self, bet):
        """ Update the bet """

        self.bet_label.configure(text="Bet: %i" % bet)

    def update_winner_paid(self, winner_paid):
        """ Print the amount paid """

        self.winner_paid_label.configure(text="Winner paid: %i" % winner_paid)

    def update_reel(self, reel, symbol):
        """ Update reel with the result """

        self.reel_labels[reel].configure(text="Reel %i: %s" % (reel, symbol))
