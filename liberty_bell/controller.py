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

        # Run the main loop
        self.ui.mainloop()

    def spin(self, message):
        """ Spin the slot machine """

        self.slot_machine.spin()
