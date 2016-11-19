import time


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

    self.update_button_state()
    self.update_display()

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

    requested_delay = 0.1

    if self.slot_machine.is_spinning:
      # Is the animation still running?
      animation_running = False

      for i, reel in enumerate(self.slot_machine.reels):
        try:
          line = reel.next_line()
          animation_running = True
          self.ui.reel_displays[i].write_line(line)
          requested_delay = 0
        except StopIteration:
          pass

      if not animation_running:
        winner = self.slot_machine.eval_spin()

        if winner:
          # Do a nice animation =)
          starting_credits = self.slot_machine.prev_credits
          ending_credits = self.slot_machine.credits

          for i, credits in enumerate(range(starting_credits + 1, ending_credits + 1)):
            self.ui.credits_led.display(credits)
            self.ui.winner_paid_led.display(i + 1)
            self.ui.buzzer.increment_tone()
            time.sleep(0.10)

        else:
          self.ui.buzzer.lose_tone()

        self.update_button_state()
        self.update_display()

    else:
      self.update_button_state()
      self.update_display()

    return requested_delay
