class Slot_Machine_Menu_Item(object):

  def __init__(self, slot_machine, ui):

    self.ui = ui
    self.slot_machine = slot_machine

  def handle_input(self, command):

    if command == "UP":
      self.slot_machine.increment_bet()
    if command == "DOWN":
      self.slot_machine.decrement_bet()
    if command == "SPIN":
      result = self.slot_machine.spin()

  def update_button_state(self):

    self.ui.menu_button.enabled = False

    self.ui.spin_button.enabled = self.slot_machine.can_spin
    self.ui.up_button.enabled = self.slot_machine.can_increase_bet
    self.ui.down_button.enabled = self.slot_machine.can_decrease_bet

    self.ui.reel1_button.enabled = False
    self.ui.reel2_button.enabled = False
    self.ui.reel3_button.enabled = False

  def update_display(self):

    self.ui.credits_led.display(self.slot_machine.credits)
    self.ui.amount_bet_led.display(self.slot_machine.bet)

    if self.slot_machine.winner_paid > 0:
      self.ui.winner_paid_led.display(self.slot_machine.winner_paid)
    else:
      self.ui.winner_paid_led.clear()

  def update(self):
    """ Update one iteration of game play """

    self.update_button_state()
    self.update_display()

    if self.slot_machine.is_spinning:
      # DO ANIMATION HERE
      self.slot_machine.eval_spin()
    else:
      pass
