import time

from config import Config
from slot_machines import Liberty_Bell_Machine
from ui import Slot_UI


class Slot_Game_Controller(object):
  """ Control the flow of play for the slot machine """

  def __init__(self):
    """ Initialize the game """

    self.slot_machine = Liberty_Bell_Machine()

    self.ui = Slot_UI(reels=self.slot_machine.reels)

    # Show a startup animation
    self.ui.startup_animation()

    # Register for UI events
    self.ui.register("menu_pressed", self, self.menu_pressed_handler)
    self.ui.register("spin_pressed", self, self.spin_pressed_handler)
    self.ui.register("up_pressed", self,
                     self.slot_machine.increment_bet)
    self.ui.register("down_pressed", self,
                     self.slot_machine.decrement_bet)

    # Register for model changes
    self.slot_machine.register(
        "credits_changed", self, self.ui.credits_led.display)
    self.slot_machine.register(
        "winner_paid_changed", self, self.ui.winner_paid_handler)
    self.slot_machine.register(
        "amount_bet_changed", self, self.ui.amount_bet_led.display)
    self.slot_machine.register(
        "spin_lose", self, self.ui.spin_lose_handler)
    self.slot_machine.register(
        "spin_completed", self, self.spin_completed_handler)

    self.ui.menu_button.enable()
    self.reset()

  def reset(self):
    """ Initialize the slot machine """

    config = Config()

    # Set up the initial credits and bet
    self.slot_machine.initialize(
        credits=config.default_credits, bet=config.default_bet)

    self.register_buttons()
    self.slot_machine.handle_state_change()

  def start(self):
    """ Start the game """

    self.ui.mainloop()

  def menu_pressed_handler(self, message):
    """ What to do when menu is pressed """

    self.ui.stop_listening()

  def register_buttons(self):
    """ Listen for button changes """

    # Register for button changes
    self.slot_machine.register(
        "enable_increase_bet", self, self.ui.up_button.enable)
    self.slot_machine.register(
        "disable_increase_bet", self, self.ui.up_button.disable)
    self.slot_machine.register(
        "enable_decrease_bet", self, self.ui.down_button.enable)
    self.slot_machine.register(
        "disable_decrease_bet", self, self.ui.down_button.disable)
    self.slot_machine.register(
        "enable_spin", self, self.ui.spin_button.enable)
    self.slot_machine.register(
        "disable_spin", self, self.ui.spin_button.disable)

  def unregister_buttons(self):
    """ Stop listening for button changes """

    self.slot_machine.unregister(
        "enable_increase_bet", self)
    self.slot_machine.unregister(
        "disable_increase_bet", self)
    self.slot_machine.unregister(
        "enable_decrease_bet", self)
    self.slot_machine.unregister(
        "disable_decrease_bet", self)
    self.slot_machine.unregister(
        "enable_spin", self)
    self.slot_machine.unregister(
        "disable_spin", self)

  def spin_pressed_handler(self, message):
    """ Respond to the spin pressed event """

    # Handle UI
    self.ui.winner_paid_led.clear()
    self.ui.spin_button.disable()
    self.ui.up_button.disable()
    self.ui.down_button.disable()

    # Stop listening for events
    self.unregister_buttons()

    # Find the result and do the animation
    result = self.slot_machine.spin()
    self.ui.show_spin(result)

    # Evaluate the results
    self.slot_machine.eval_spin(result)

  def spin_completed_handler(self, result):
    """ Enable the buttons and wait for next input """

    self.ui.spin_button.disable()
    self.ui.up_button.disable()
    self.ui.down_button.disable()

    self.register_buttons()

    self.slot_machine.handle_state_change()

    self.ui.mainloop()
