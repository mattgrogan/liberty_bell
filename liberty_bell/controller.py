from machine import Liberty_Bell_Machine

class Slot_Game_Controller(object):
    """ Control the flow of play for the slot machine """

    def __init__(self):
        """ Initialize the game """

        self.slot_machine = Liberty_Bell_Machine()

    def spin(self):
        """ Spin the slot machine """

        self.slot_machine.spin()
