from machine import Liberty_Bell_Machine
from gui import Slot_GUI


class Slot_Game_Controller(object):
    """ Control the flow of play for the slot machine """

    def __init__(self):
        """ Initialize the game """

        self.slot_machine = Liberty_Bell_Machine()
        self.ui = Slot_GUI()

        # Register for events
        self.ui.register("SPIN_BUTTON_PRESSED", self, self.spin)
        self.slot_machine.register("PAYOUT", self, self.credits_changed)
        self.slot_machine.register("PLACE_BET", self, self.credits_changed)


        # Run the main loop
        self.ui.mainloop()

    def spin(self, message):
        """ Spin the slot machine """

        result = self.slot_machine.spin()

        self.ui.update_winner_paid(result.winner_paid)

        for i, symbol in enumerate(result.reels):
            self.ui.update_reel(i, symbol)

    def credits_changed(self, credits):
        """ Callback for change in credits """

        self.ui.update_credits(credits)
