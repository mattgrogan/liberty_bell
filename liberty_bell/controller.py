import time

from events import Events
from slot_machines import Liberty_Bell_Machine
from ui import Slot_UI


class Slot_Game_Controller(object):
  """ Control the flow of play for the slot machine """

  def __init__(self, ui):
    """ Initialize the game """

    self.slot_machine = Liberty_Bell_Machine()

    if ui == "TEXT_UI":
      from user_interfaces.text_ui import Slot_Text_UI
      self.ui = Slot_Text_UI(reels=self.slot_machine.reels)
    elif ui == "GUI_UI":
      from user_interfaces.gui import Slot_GUI
      self.ui = Slot_GUI(reels=self.slot_machine.reels)
    elif ui == "RPI_UI":
      from user_interfaces.rpi_ui import Slot_RPI_UI
      self.ui = Slot_RPI_UI(reels=self.slot_machine.reels)
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
        Events.PAYOUT, self, self.ui.update_winner_paid)
    self.slot_machine.register(
        Events.BET_CHANGED, self, self.ui.update_bet)
    self.slot_machine.register(
        Events.SPIN_EVAL, self, self.on_evaluate_spin)

    # Set up the initial credits and bet
    self.slot_machine.initialize(credits=100, bet=1)

    # Show a startup animation
    self.ui.startup_animation()

    # time.sleep(2)

    # Run the main loop
    self.ui.spin_button.enable()
    self.ui.up_button.enable()
    self.ui.down_button.enable()

    self.ui.listen_for_input()

  def spin(self, message):
    """ Spin the slot machine """

    self.ui.clear_winner_paid()

    self.ui.spin_button.disable()
    self.ui.up_button.disable()
    self.ui.down_button.disable()

    # Find the result and do the animation
    result = self.slot_machine.spin()
    self.ui.show_spin(result)

    # Evaluate the results
    self.slot_machine.eval_spin(result)

  def on_evaluate_spin(self, result):
    """ Evaluate the spin """

    # Now we can set the ui to ready again
    self.ui.spin_button.enable()
    self.ui.up_button.enable()
    self.ui.down_button.enable()

    self.ui.listen_for_input()
