import time


class Ready_State(object):
  """ The slot machine is ready for a spin """

  def __init__(self, controller, ui, slot_machine):
    """ Initialize the state """

    self.controller = controller
    self.ui = ui
    self.slot_machine = slot_machine

  def enable_buttons(self):
    """ Enable buttons if they're allowed """

    self.ui.menu_button.enable()

    if self.slot_machine.can_spin:
      self.ui.spin_button.enable()
    else:
      self.ui.spin_button.disable()

    if self.slot_machine.can_increase_bet:
      self.ui.up_button.enable()
    else:
      self.ui.up_button.disable()

    if self.slot_machine.can_decrease_bet:
      self.ui.down_button.enable()
    else:
      self.ui.down_button.disable()

    # We're not using the reel buttons
    self.ui.reel1_button.disable()
    self.ui.reel2_button.disable()
    self.ui.reel3_button.disable()

  def up_pressed_handler(self):
    """ Increase the bet """

    self.controller.slot_machine.increment_bet()

  def down_pressed_handler(self):
    """ Decrease the bet """

    self.controller.slot_machine.decrement_bet()

  def spin_pressed_handler(self):
    """ Spin the reels """

    # Clear the winner paid
    self.ui.winner_paid_led.clear()

    # Change the state to Spinning_State
    self.controller.current_state = self.controller.spinning_state
    self.controller.current_state.enable_buttons()

    # Find the result and do the animation
    result = self.controller.slot_machine.spin()
    self.ui.show_spin(result)

    # Evaluate the results
    self.controller.slot_machine.eval_spin(result)


class Spinning_State(object):
  """ The spin button was pressed and we're in the spinning state """

  def __init__(self, controller, ui, slot_machine):
    """ Initialize the state """

    self.controller = controller
    self.ui = ui
    self.slot_machine = slot_machine

  def spin_completed_handler(self):
    """ Spin is complete, move to ready state """

    self.controller.current_state = self.controller.ready_state
    self.controller.current_state.enable_buttons()

  def enable_buttons(self):
    """ No buttons allowed """

    self.ui.spin_button.disable()
    self.ui.up_button.disable()
    self.ui.down_button.disable()
    self.ui.menu_button.disable()

    # We're not using the reel buttons
    self.ui.reel1_button.disable()
    self.ui.reel2_button.disable()
    self.ui.reel3_button.disable()


class Slot_Game_Controller(object):
  """ Control the flow of play for the slot machine """

  def __init__(self, ui, slot_machine):
    """ Initialize the game """

    # Connect to the slot machine
    self.slot_machine = slot_machine
    self.slot_machine.register(
        "spin_completed", self, self.spin_completed_handler)
    self.slot_machine.register(
        "state_changed", self, self.state_changed_handler)

    self.action = None

    self.ui = ui

    self.ui.reels = self.slot_machine.reels

    self.ready_state = Ready_State(self, ui, slot_machine)
    self.spinning_state = Spinning_State(self, ui, slot_machine)

    self.current_state = self.ready_state

  def initialize_ui(self):
    """ Set up the UI """

    self.action = None
    self.current_state.enable_buttons()
    self.update_display()

  def spin_pressed_handler(self, e=None):
    """ Handle the spin button """

    self.current_state.spin_pressed_handler()

  def up_pressed_handler(self, e=None):
    """ Handle the up button """

    self.current_state.up_pressed_handler()

  def down_pressed_handler(self, e=None):
    """ Handle the down button """

    self.current_state.down_pressed_handler()

  def menu_pressed_handler(self, e=None):
    """ Handle menu pressed """

    self.action = "menu"

  def b1_pressed_handler(self, e=None):
    """ Handle the button """

    self.current_state.b1_pressed_handler()

  def b2_pressed_handler(self, e=None):
    """ Handle the button """

    self.current_state.b2_pressed_handler()

  def b3_pressed_handler(self, e=None):
    """ Handle the button """

    pass

  def spin_completed_handler(self, e=None):
    """ Handle the spin completion """

    self.current_state.spin_completed_handler()

  def state_changed_handler(self, e=None):
    """ Update any of the data on the display """

    self.update_display()

  def update_display(self):
    """ Update the display with current info """

    self.ui.credits_led.display(self.slot_machine.credits)
    self.ui.amount_bet_led.display(self.slot_machine.bet)

    if self.slot_machine.winner_paid > 0:
      self.ui.winner_paid_led.display(self.slot_machine.winner_paid)
    else:
      self.ui.winner_paid_led.clear()

    self.current_state.enable_buttons()
    self.ui.menu_display.clear()
    self.ui.menu_display.display()

    self.ui.menu_display.text("Press SPIN")
    self.ui.menu_display.display()
