class Menu_Controller(object):

  def __init__(self, ui):

    self.name = "Menu"
    self.ui = ui
    self.menu_item = None
    self._options = None
    self._current_option = 0

  def start(self, menu_item):

    self.menu_item = menu_item
    self._options = self.menu_item.options
    self._current_option = 0

    self.update_button_state()

  def set_options(self, options):
    # Set the available options
    self._options = options
    self._options.append(("Exit Game", self.exit))

  def handle_input(self, command):

    if command == "SPIN":

  def update_button_state(self):

    self.ui.menu_button.enabled = True
    self.ui.spin_button.enabled = True
    self.ui.up_button.enabled = True
    self.ui.down_button.enabled = True

    self.ui.reel1_button.enabled = False
    self.ui.reel2_button.enabled = False
    self.ui.reel3_button.enabled = False

  def stop(self):

    for display in self.ui.reel_displays:
      display.clear()

    self.ui.amount_bet_led.clear()
    self.ui.winner_paid_led.clear()
    self.ui.credits_led.clear()

  def exit(self):
    print "Exiting..."

  def update(self):
    """ Update one iteration of game play """

    requested_delay_ms = 100
    return requested_delay_ms
