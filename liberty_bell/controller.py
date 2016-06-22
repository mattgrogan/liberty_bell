from machine import Liberty_Bell_Machine
from gui import Slot_GUI
from events import Events


class Slot_Game_Controller(object):
    """ Control the flow of play for the slot machine """

    def __init__(self):
        """ Initialize the game """

        self.slot_machine = Liberty_Bell_Machine()
        self.ui = Slot_GUI()

        # Register for UI events
        self.ui.register(Events.SPIN, self, self.spin)
        self.ui.register(Events.INCREMENT_BET, self, self.slot_machine.increment_bet)
        self.ui.register(Events.DECREMENT_BET, self, self.slot_machine.decrement_bet)

        # Register for model changes
        self.slot_machine.register(Events.CREDITS_CHANGED, self, self.ui.update_credits)
        self.slot_machine.register(Events.BET_CHANGED, self, self.ui.update_bet)

        # Set up the initial credits and bet
        self.slot_machine.initialize(credits=100, bet=1)

        # Run the main loop
        self.ui.mainloop()

    def spin(self, message):
        """ Spin the slot machine """

        result = self.slot_machine.spin()

        self.ui.update_winner_paid(result.winner_paid)

        for i, symbol in enumerate(result.reels):
            self.ui.update_reel(i, symbol)