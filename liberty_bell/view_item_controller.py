class View_Item_Controller(object):
  """ Controller to view all items on a reel """

  def __init__(self, ui, slot_machine):
    """ Initialize the controller """

    self.ui = ui
    self.slot_machine = slot_machine

  def initialize_ui(self):
    """ Only the three reel buttons are in use """

    self.ui.spin_button.disable()
    self.ui.up_button.disable()
    self.ui.down_button.disable()
    self.ui.reel1_button.enable()
    self.ui.reel2_button.enable()
    self.ui.reel3_button.enable()

    self.ui.credits_led.clear()
    self.ui.winner_paid_led.clear()
    self.ui.amount_bet_led.clear()

    self.action = None

    self.ui.display_1.clear()
    self.ui.display_2.clear()
    self.ui.display_3.clear()

  def display(self, reel):
    """ Display current image on reel """

    image = self.slot_machine.reels[reel].current_symbol().image

    if reel == 0:
      self.ui.display_1.display_image(image)
    if reel == 1:
      self.ui.display_2.display_image(image)
    if reel == 2:
      self.ui.display_3.display_image(image)

  def menu_pressed_handler(self, e=None):
    """ Handle the button """

    self.action = "menu"

  def b1_pressed_handler(self, e=None):
    """ Handle the button """

    self.slot_machine.reels[0].advance()
    self.display(0)

  def b2_pressed_handler(self, e=None):
    """ Handle the button """

    self.slot_machine.reels[1].advance()
    self.display(1)

  def b3_pressed_handler(self, e=None):
    """ Handle the button """

    self.slot_machine.reels[2].advance()
    self.display(2)
