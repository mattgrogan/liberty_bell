import Tkinter as tk
from PIL import ImageTk
from events import Events
from ui import Slot_UI
import time


class Slot_GUI(Slot_UI, tk.Tk):
    """ Prototype GUI for the slot machine """

    def __init__(self, reels=None, **kwargs):
        """ Initialize the GUI """

        super(Slot_GUI, self).__init__(None, **kwargs)
        tk.Tk.__init__(self, None, **kwargs)

        self.reels = reels
        self.current_stops = [0] * len(self.reels)

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
        self.reel_labels = []
        for i in range(len(self.reels)):
            img = ImageTk.PhotoImage(self.reels[i].stops[self.current_stops[i]].image)
            reel_label = tk.Label(self, image=img)
            reel_label.image = img
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

        im = ImageTk.PhotoImage(symbol.image)

        self.reel_labels[reel].configure(image=im)
        self.reel_labels[reel].image = im

    def show_reel_spin(self, result):
        """ Animate the spin """

        REEL = 0

        winning_symbol = result.reels[REEL]

        # Must go around once
        self.reels[REEL].reset(required_spins=1)

        while self.reels[REEL].has_next(winning_symbol):
            im = ImageTk.PhotoImage(self.reels[REEL].get_current_symbol().image)
            self.reel_labels[REEL].configure(image=im)
            self.reel_labels[REEL].image = im
            time.sleep(0.25)
            self.update()
