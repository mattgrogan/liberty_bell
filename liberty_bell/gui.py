import Tkinter as tk


class Slot_GUI(tk.Tk):
    """ Prototype GUI for the slot machine """

    def __init__(self, *args, **kwargs):
        """ Initialize the GUI """

        tk.Tk.__init__(self, *args, **kwargs)

        # Add the spin button
        self.button = tk.Button(self, text="SPIN", command=self.spin_pressed)
        self.button.pack(side=tk.RIGHT)

        self.winner_paid_label = tk.Label(self, text="Winner paid: 0")
        self.winner_paid_label.pack()

        self.credits_label = tk.Label(self, text="Credits: 0")
        self.credits_label.pack()

        self.bet_label = tk.Label(self, text="Bet: 0")
        self.bet_label.pack()

        nbr_reels = 3
        self.reel_labels = []
        for i in range(nbr_reels):
            reel_label = tk.Label(self, text="Reel %i: " % i)
            reel_label.pack()
            self.reel_labels.append(reel_label)

        # Set up events
        events = ["SPIN_BUTTON_PRESSED"]

        self.events = {event: dict() for event in events}

    def _get_subscribers(self, event):
        """ Get the subscribers for a particular event """

        return self.events[event]

    def register(self, event, who, callback=None):
        """ Register for updates """

        if callback is None:
            callback = getattr(who, 'update')

        self._get_subscribers(event)[who] = callback

    def spin_pressed(self):
        """ Raise a notification to respond to the spin button pressed event """

        message = None
        subscribers = self._get_subscribers("SPIN_BUTTON_PRESSED")

        for subscriber, callback in subscribers.iteritems():
            callback(message)

    def update_winner_paid(self, winner_paid):
        """ Print the amount paid """

        self.winner_paid_label.configure(text = "Winner paid: %i" % winner_paid)

    def update_reel(self, reel, symbol):
        """ Update reel with the result """

        self.reel_labels[reel].configure(text = "Reel %i: %s" % (reel, symbol))

    def update_credits(self, credits):
        """ Update the credits box """

        self.credits_label.configure(text = "Credits: %i" % credits)

    def update_bet(self, bet):
        """ Update the bet """

        self.bet_label.configure(text = "Bet: %i" % bet)
