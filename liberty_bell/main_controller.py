from liberty_bell.menu import Menu


class Main_Controller(Menu):
  """ This is the main controller for the game. """

  def __init__(self, *args, **kwargs):
    super(Main_Controller, self).__init__(*args, **kwargs)

  def handle_input(self, command):

    next_item = self.current_item.handle_input(command)

    if next_item is None:
      self.move()

    if next_item != self.current_item:
      self.current_item.stop()
      self.current_item = next_item
      self.current_item.start()

  def handle_spin(self, message=None):
    self.handle_input("SPIN")

  def handle_up(self, message=None):
    self.handle_input("UP")

  def handle_down(self, message=None):
    self.handle_input("DOWN")

  def handle_b1(self, message=None):
    self.handle_input("B1")

  def handle_b2(self, message=None):
    self.handle_input("B2")

  def handle_b3(self, message=None):
    self.handle_input("B3")

  def handle_menu(self, message=None):
    self.handle_input("MENU")

  def run(self):
    return self.current_item.update()
