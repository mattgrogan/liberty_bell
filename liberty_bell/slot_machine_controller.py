import time


class Buy_Credits_Cmd(object):

  def __init__(self, ui, slot_machine, controller, amount):
    self.ui = ui
    self.slot_machine = slot_machine
    self.controller = controller
    self.amount = amount

  def execute(self, action):

    if action == "ACTION_LABEL":
      message = "Buy %i credit(s)" % self.amount
      self.ui.menu_display.clear()
      self.ui.menu_display.add_line(message)
      self.ui.menu_display.flush()

    if action == "ACTION_DISPLAY":
      message = "Buying %i Press SPIN" % self.amount
      self.ui.menu_display.clear()
      self.ui.menu_display.add_line(message)
      self.ui.menu_display.flush()

    if action == "ACTION_TRIGGER":
      self.slot_machine.credits += self.amount
      self.controller.update_display()


class Toggle_Autoplay_Cmd(object):

  def __init__(self, ui, controller):
    self.ui = ui
    self.controller = controller

  def execute(self, action):
    message = "Autoplay: "

    autoplay = self.controller.options["AUTOPLAY"]

    if action == "ACTION_LABEL":
      message += "ON" if autoplay else "OFF"
      self.ui.menu_display.clear()
      self.ui.menu_display.add_line(message)
      self.ui.menu_display.flush()

    if action == "ACTION_DISPLAY":
      message = "Press SPIN to Save"
      self.ui.menu_display.clear()
      self.ui.menu_display.add_menu_text(message, headline="CONFIRM?")
      self.ui.menu_display.flush()

    if action == "ACTION_TRIGGER":
      self.controller.options["AUTOPLAY"] = not autoplay

# TODO: Move this to UI
class Update_Display_Cmd(object):

  def __init__(self, ui, text):
    self.ui = ui
    self.text = text

  def execute(self, action):
    print "Received action %s from '%s'" % (action, self.text)

    if action == "ACTION_LABEL":
      self.ui.menu_display.clear()
      self.ui.menu_display.add_menu_text(self.text)
      self.ui.menu_display.flush()


class Slot_Machine_Controller(object):

  def __init__(self, slot_machine, ui):

    self.ui = ui
    self.slot_machine = slot_machine
    self.options = {}
    self.options["AUTOPLAY"] = False

    self.user_opts = []

    # Options for purchasing credits
    self.user_opts.append(Buy_Credits_Cmd(self.ui, self.slot_machine, self, 1))
    self.user_opts.append(Buy_Credits_Cmd(self.ui, self.slot_machine, self, 10))
    self.user_opts.append(Buy_Credits_Cmd(self.ui, self.slot_machine, self, 100))

    self.user_opts.append(Toggle_Autoplay_Cmd(self.ui, self))



  @property
  def name(self):
    return self.slot_machine.name

  def get_command(self, command_name, label, params=None):

    if command_name == "BUY_CREDITS":
      cmd = Buy_Credits_Cmd(self.ui, self.slot_machine, self, params)
    elif command_name == "TOGGLE_AUTOPLAY":
      cmd = Toggle_Autoplay_Cmd(self.ui, self)
    elif command_name == "UPDATE_DISPLAY":
      cmd = Update_Display_Cmd(self.ui, label)

    return cmd

  def handle_input(self, command):

    if command == "MENU":
      return self.options
    if command == "UP":
      self.slot_machine.increment_bet()
    if command == "DOWN":
      self.slot_machine.decrement_bet()
    if command == "SPIN":
      if self.slot_machine.can_spin:
        self.ui.buzzer.button_tone()
        self.slot_machine.spin()

    self.update_button_state()
    self.update_display()

    return self

  def update_button_state(self):

    self.ui.menu_button.enabled = not self.slot_machine.is_spinning

    self.ui.spin_button.enabled = self.slot_machine.can_spin
    self.ui.up_button.enabled = self.slot_machine.can_increase_bet
    self.ui.down_button.enabled = self.slot_machine.can_decrease_bet

    self.ui.reel1_button.enabled = False
    self.ui.reel2_button.enabled = False
    self.ui.reel3_button.enabled = False

  def update_display(self):

    self.ui.menu_display.clear()
    self.ui.menu_display.add_wrapped_text(self.name)
    self.ui.menu_display.flush()

    self.ui.credits_led.display(self.slot_machine.credits)
    self.ui.amount_bet_led.display(self.slot_machine.bet)

    if self.slot_machine.winner_paid > 0:
      self.ui.winner_paid_led.display(self.slot_machine.winner_paid)
    else:
      self.ui.winner_paid_led.clear()

  def start(self):
    self.update_button_state()
    self.update_display()

  def stop(self):

    for display in self.ui.reel_displays:
      display.clear()

    self.ui.amount_bet_led.clear()
    self.ui.winner_paid_led.clear()
    self.ui.credits_led.clear()

  def update(self):
    """ Update one iteration of game play """

    requested_delay_ms = 100

    if self.slot_machine.is_spinning:
      # Is the animation still running?
      animation_running = False

      for i, reel in enumerate(self.slot_machine.reels):
        try:
          line = reel.next_line()
          animation_running = True
          self.ui.reel_displays[i].write_line(line)
          requested_delay_ms = 0
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

      if self.options["AUTOPLAY"]:
        # TODO: Give a pause and allow player to enter the menu again
        self.handle_input("SPIN")

    return requested_delay_ms
