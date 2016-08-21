import time

from events import Events
from slot_machines import Liberty_Bell_Machine
from ui import Slot_UI


class Slot_Game_Controller(object):
  """ Control the flow of play for the slot machine """

  def __init__(self):
    """ Initialize the game """

    self.slot_machine = Liberty_Bell_Machine()

    self.ui = Slot_UI(reels=self.slot_machine.reels)

    # Register for UI events
    self.ui.register("spin_pressed", self, self.spin_pressed_handler)
    self.ui.register("up_pressed", self,
                     self.slot_machine.increment_bet)
    self.ui.register("down_pressed", self,
                     self.slot_machine.decrement_bet)

    # Register for model changes
    self.slot_machine.register(
        "credits_changed", self, self.ui.credits_led.display)
    self.slot_machine.register(
        "winner_paid_changed", self, self.ui.winner_paid_led.display)
    self.slot_machine.register(
        "amount_bet_changed", self, self.ui.amount_bet_led.display)
    self.slot_machine.register(
        "spin_completed", self, self.spin_completed_handler)

    # Set up the initial credits and bet
    self.slot_machine.initialize(credits=100, bet=1)

    # Show a startup animation
    self.ui.startup_animation()

    # time.sleep(2)

    # Run the main loop
    self.ui.spin_button.enable()
    self.ui.up_button.enable()
    self.ui.down_button.enable()

    self.ui.mainloop()

  def spin_pressed_handler(self, message):
    """ Respond to the spin pressed event """

    self.ui.winner_paid_led.clear()

    self.ui.spin_button.disable()
    self.ui.up_button.disable()
    self.ui.down_button.disable()

    # Find the result and do the animation
    result = self.slot_machine.spin()
    self.ui.show_spin(result)

    # Evaluate the results
    self.slot_machine.eval_spin(result)

  def spin_completed_handler(self, result):
    """ Enable the buttons and wait for next input """

    # Now we can set the ui to ready again
    self.ui.spin_button.enable()
    self.ui.up_button.enable()
    self.ui.down_button.enable()

    self.ui.mainloop()
