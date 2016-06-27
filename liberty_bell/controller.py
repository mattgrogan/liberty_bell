from slot_machines import Liberty_Bell_Machine
from ui import Slot_UI
from user_interfaces.text_ui import Slot_Text_UI
from user_interfaces.rpi_ui import Slot_RPI_UI
from events import Events


class Slot_Game_Controller(object):
    """ Control the flow of play for the slot machine """

    def __init__(self, ui):
        """ Initialize the game """

        self.slot_machine = Liberty_Bell_Machine()

        if ui == "TEXT_UI":
            self.ui = Slot_Text_UI()
        elif ui == "GUI_UI":
            self.ui = Slot_GUI()
	elif ui == "RPI_UI":
	    self.ui = Slot_RPI_UI()
        else:
            raise Exception("Invalid UI: " % ui)

        # Register for UI events
        self.ui.register(Events.SPIN, self, self.spin)
        self.ui.register(Events.INCREMENT_BET, self,
                         self.slot_machine.increment_bet)
        self.ui.register(Events.DECREMENT_BET, self,
                         self.slot_machine.decrement_bet)

        # Register for model changes
        self.slot_machine.register(
            Events.CREDITS_CHANGED, self, self.ui.update_credits)
        self.slot_machine.register(
            Events.BET_CHANGED, self, self.ui.update_bet)

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
